"""
Phase 1 (BUILD_SPEC.md §6): agent joins a room, transcribes human speakers,
logs interim/final transcripts with detected language. No translation, no
TTS, no audio published yet.
"""

import asyncio
import logging

import numpy as np

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, JobRequest, WorkerOptions, cli, stt
from livekit.plugins import openai

from config import AGENT_IDENTITY, AGENT_NAME

load_dotenv()

logger = logging.getLogger("sema-interpreter-agent")

stt_provider = openai.STT(detect_language=True)


def is_agent(participant: rtc.RemoteParticipant) -> bool:
    # "translator" kept for the echo guard during migration (docs/naming_spec.md §8
    # backward compatibility: legacy service ID may remain as an internal alias).
    return participant.identity == AGENT_IDENTITY or participant.identity.startswith(
        ("sema-interpreter", "translator")
    )


async def transcribe_track(participant: rtc.RemoteParticipant, track: rtc.Track) -> None:
    audio_stream = rtc.AudioStream(track, sample_rate=24000, num_channels=1)
    stt_stream = stt_provider.stream()

    async def forward() -> None:
        async for ev in stt_stream:
            logger.info("DEBUG raw event: %s", ev.type)
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

    forward_task = asyncio.create_task(forward())
    frame_count = 0
    try:
        async for ev in audio_stream:
            frame_count += 1
            if frame_count % 50 == 0:
                samples = np.frombuffer(ev.frame.data, dtype=np.int16)
                rms = float(np.sqrt(np.mean(samples.astype(np.float64) ** 2))) if len(samples) else 0.0
                logger.info(
                    "DEBUG pushed %d audio frames, sample_rate=%s, rms=%.1f",
                    frame_count, ev.frame.sample_rate, rms,
                )
            stt_stream.push_frame(ev.frame)
    finally:
        await stt_stream.aclose()
        await forward_task


async def entrypoint(ctx: JobContext) -> None:
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
        asyncio.create_task(transcribe_track(participant, track))

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)


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
