# sema-interpreter-agent (Phase 2)

Standalone LiveKit Agents worker for **Sema Interpreter** (canonical naming:
see `../docs/naming_spec.md`). Joins a meeting room, subscribes to human
speakers' audio, runs streaming STT (OpenAI, language auto-detect), translates
each final segment into one hard-coded target language, and publishes the
synthesized speech back into the room as a single `translation-en` track —
see `BUILD_SPEC.md` §6 Phase 2.

## Status (2026-07-13)

Phase 1 (transcription) is verified. Phase 2 (translate + speak back, one
language) is coded but **not yet verified live**: the `OPENAI_API_KEY` in
`.env` authenticates but has no usable quota (`429 insufficient_quota` on
chat/TTS calls), so translate/TTS calls fail until billing is added to the
account. Switching to Groq or NVIDIA Riva was considered as a cheaper/free
alternative and ruled out: Groq TTS only supports English/Arabic, NVIDIA Riva
TTS has no Hindi or Telugu — neither covers the required Hindi/Spanish/Telugu
set (see `BUILD_SPEC.md` §3).

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

## Join a real meeting room (Phase 2 test)

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

## Phase 2 acceptance

Speak in the real meeting → a listener hears an English translation of the
speech through the actual Zoiko call (via the `translation-en` track). Blocked
on a funded `OPENAI_API_KEY` — see Status above. Stop here — do not fan out to
all target languages (Phase 3+) until this passes.
