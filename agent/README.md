# sema-interpreter-agent (Phase 1)

Standalone LiveKit Agents worker for **Sema Interpreter** (canonical naming:
see `../docs/naming_spec.md`). Joins a meeting room, subscribes to human
speakers' audio, runs streaming STT (OpenAI, language auto-detect), and logs
transcripts. No translation, no TTS, no published audio yet — see
`BUILD_SPEC.md` §6 Phase 1.

## Status (2026-07-13)

Environment is set up and the worker connects to LiveKit successfully. A
real `OPENAI_API_KEY` is now in `.env` — ready to verify Phase 1 acceptance
(real transcripts from real speech). Switching to Groq was considered and
rejected: Groq TTS only supports English/Arabic, not the Hindi/Spanish/Telugu
this project needs (see `BUILD_SPEC.md` §3).

## Setup

Requires Python 3.10+ (livekit-agents uses `typing.TypeAlias`, unavailable on 3.9).

```bash
cd agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in LIVEKIT_URL / LIVEKIT_API_KEY / LIVEKIT_API_SECRET / OPENAI_API_KEY
```

Reuse the same `LIVEKIT_URL` / `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` the
Zoiko Sema server already uses — no new credentials.

## Run the worker

```bash
python interpreter_agent.py dev
```

This starts the worker with **explicit dispatch** (`agent_name=sema-interpreter-agent`,
set via `AGENT_NAME` in `.env`). The worker does not auto-join every room; a
room only gets the agent when a job is explicitly dispatched to it, and the
room name is supplied at dispatch time — not hardcoded in this repo.

## Join a real meeting room (Phase 1 test)

Dispatch the agent into the same room the Zoiko client is already in, using
the LiveKit CLI:

```bash
lk dispatch create \
  --room <the-meeting-room-name> \
  --agent-name sema-interpreter-agent
```

`<the-meeting-room-name>` is whatever room name the Zoiko client used to join
(from `meetingRoomPath(code)` in the main Zoiko repo). The agent joins that
room, subscribes to human mics only, and logs transcripts to the worker's
console.

## Phase 1 acceptance

Speak in the real meeting → see accurate interim/final transcripts with
detected language in the worker logs. Stop here — do not add translation or
TTS (Phase 2+).
