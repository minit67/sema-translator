"""
Phase 1 (BUILD_SPEC.md §6): agent joins a room, transcribes human speakers,
logs interim/final transcripts with detected language. No translation, no
TTS, no audio published yet.
"""

import asyncio
import logging

from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, JobRequest, WorkerOptions, cli, stt
from livekit.plugins import openai

from config import AGENT_IDENTITY, AGENT_NAME

logger = logging.getLogger("translator-agent")

stt_provider = openai.STT(detect_language=True, use_realtime=True)


def is_agent(participant: rtc.RemoteParticipant) -> bool:
    return participant.identity == AGENT_IDENTITY or participant.identity.startswith(
        "translator"
    )


async def transcribe_track(participant: rtc.RemoteParticipant, track: rtc.Track) -> None:
    audio_stream = rtc.AudioStream(track)
    stt_stream = stt_provider.stream()

    async def forward() -> None:
        async for ev in stt_stream:
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
    try:
        async for ev in audio_stream:
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
