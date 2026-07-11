# sema-translator

Standalone home for the **translator agent** (Python) used by Zoiko Sema's
parallel AI voice translation feature. This repo holds only the agent — the
client and server live in the separate Zoiko Sema repo.

- Full plan and phase breakdown: [`BUILD_SPEC.md`](BUILD_SPEC.md)
- Agent setup and run instructions: [`agent/README.md`](agent/README.md)

## Status

Phase 1 (agent joins a room and transcribes speakers) is scaffolded and the
worker connects to LiveKit successfully, but is blocked on a real
`OPENAI_API_KEY` for actual transcription. See `agent/README.md` and
`BUILD_SPEC.md` §3 for details, including why Groq was considered and ruled
out as a substitute provider.
