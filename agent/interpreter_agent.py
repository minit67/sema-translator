"""
Phase 2 (BUILD_SPEC.md §6): agent joins a room, transcribes human speakers,
translates each final segment into one hard-coded target language, and
publishes the synthesized speech as a single `translation-<lang>` track.
"""

import asyncio
import json
import logging

import numpy as np
import openai as openai_sdk

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, JobRequest, WorkerOptions, cli, stt
from livekit.plugins import openai

from config import AGENT_IDENTITY, AGENT_NAME, PHASE2_TARGET_LANG

load_dotenv()

logger = logging.getLogger("sema-interpreter-agent")

stt_provider = openai.STT(detect_language=True)
tts_provider = openai.TTS()
translate_client = openai_sdk.AsyncOpenAI()

# Identity contract from docs/naming_spec.md §5 — published as this participant's
# metadata so the meeting client can render it as an AI service (no camera/mic
# controls, excluded from human attendee counts) without guessing from identity.
IDENTITY_METADATA = json.dumps(
    {
        "entity_type": "AI_SERVICE",
        "service_kind": "INTERPRETER",
        "service_id": AGENT_IDENTITY,
        "feature_key": "live_interpretation",
        "counts_as_human_participant": False,
        "has_camera_capability": False,
        "has_user_microphone_control": False,
        "is_recording_actor": False,
        "policy_managed": True,
    }
)


def is_agent(participant: rtc.RemoteParticipant) -> bool:
    # "translator" kept for the echo guard during migration (docs/naming_spec.md §8
    # backward compatibility: legacy service ID may remain as an internal alias).
    return participant.identity == AGENT_IDENTITY or participant.identity.startswith(
        ("sema-interpreter", "translator")
    )


async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    resp = await translate_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    f"Translate the user's message from {source_lang} to "
                    f"{target_lang}. Reply with only the translated text — "
                    "no quotes, no explanation."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content.strip()


async def speak_translation(audio_source: rtc.AudioSource, text: str) -> None:
    async for synthesized in tts_provider.synthesize(text):
        await audio_source.capture_frame(synthesized.frame)


async def translate_and_speak(
    participant: rtc.RemoteParticipant,
    text: str,
    source_lang: str,
    audio_source: rtc.AudioSource,
) -> None:
    if source_lang == PHASE2_TARGET_LANG:
        return
    for attempt in (1, 2):
        try:
            translated = await translate_text(text, source_lang, PHASE2_TARGET_LANG)
            logger.info(
                "[%s] (%s) translated: %s", participant.identity, PHASE2_TARGET_LANG, translated
            )
            await speak_translation(audio_source, translated)
            return
        except Exception:
            if attempt == 2:
                logger.exception("translate/speak failed for %s", participant.identity)
            else:
                logger.warning(
                    "translate/speak failed for %s, retrying once", participant.identity
                )


async def translation_worker(queue: asyncio.Queue, audio_source: rtc.AudioSource) -> None:
    # Single consumer processes finished segments strictly in the order they
    # were spoken. Translation latency varies per segment, so fanning these
    # out as independent tasks (the previous approach) let a fast translation
    # of a later sentence jump the queue and play before an earlier one —
    # audible as translations arriving out of order once more than one
    # speaker (or fast consecutive sentences) are involved.
    while True:
        participant, text, source_lang = await queue.get()
        await translate_and_speak(participant, text, source_lang, audio_source)


async def transcribe_track(
    participant: rtc.RemoteParticipant,
    track: rtc.Track,
    translation_queue: asyncio.Queue,
) -> None:
    audio_stream = rtc.AudioStream(track, sample_rate=24000, num_channels=1)
    stt_stream = stt_provider.stream()

    async def forward() -> None:
        async for ev in stt_stream:
            logger.debug("raw STT event: %s", ev.type)
            if ev.type == stt.SpeechEventType.INTERIM_TRANSCRIPT:
                alt = ev.alternatives[0]
                logger.info(
                    "[%s] (%s, interim) %s", participant.identity, alt.language, alt.text
                )
            elif ev.type == stt.SpeechEventType.FINAL_TRANSCRIPT:
                alt = ev.alternatives[0]
                logger.info(
                    "[%s] (%s, final) %s", participant.identity, alt.language, alt.text
                )
                if alt.text.strip():
                    translation_queue.put_nowait((participant, alt.text, alt.language))

    forward_task = asyncio.create_task(forward())
    frame_count = 0
    try:
        async for ev in audio_stream:
            frame_count += 1
            if frame_count % 50 == 0:
                samples = np.frombuffer(ev.frame.data, dtype=np.int16)
                rms = float(np.sqrt(np.mean(samples.astype(np.float64) ** 2))) if len(samples) else 0.0
                logger.debug(
                    "pushed %d audio frames, sample_rate=%s, rms=%.1f",
                    frame_count, ev.frame.sample_rate, rms,
                )
            stt_stream.push_frame(ev.frame)
    finally:
        await stt_stream.aclose()
        await forward_task


async def entrypoint(ctx: JobContext) -> None:
    audio_source = rtc.AudioSource(
        sample_rate=tts_provider.sample_rate, num_channels=tts_provider.num_channels
    )
    translation_track = rtc.LocalAudioTrack.create_audio_track(
        f"translation-{PHASE2_TARGET_LANG}", audio_source
    )
    translation_queue: asyncio.Queue = asyncio.Queue()

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.TrackPublication,
        participant: rtc.RemoteParticipant,
    ) -> None:
        if track.kind != rtc.TrackKind.KIND_AUDIO:
            return
        if is_agent(participant):
            return
        logger.info("subscribing STT to participant: %s", participant.identity)
        asyncio.create_task(transcribe_track(participant, track, translation_queue))

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    await ctx.room.local_participant.set_metadata(IDENTITY_METADATA)
    await ctx.room.local_participant.publish_track(
        translation_track,
        rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE),
    )
    logger.info("published translation-%s track", PHASE2_TARGET_LANG)
    asyncio.create_task(translation_worker(translation_queue, audio_source))


async def request_fnc(req: JobRequest) -> None:
    # fixed identity so the echo guard (is_agent) can key off it
    await req.accept(name=AGENT_NAME, identity=AGENT_IDENTITY)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            request_fnc=request_fnc,
            agent_name=AGENT_NAME,
        )
    )
