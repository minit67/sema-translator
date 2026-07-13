# sema-translator

Standalone home for the **Sema Interpreter agent** (Python) used by Zoiko
Sema's parallel AI voice translation feature. This repo holds only the agent
— the client and server live in the separate Zoiko Sema repo.

- Canonical naming, UI, and identity spec: [`docs/naming_spec.md`](docs/naming_spec.md)
- Full plan and phase breakdown: [`BUILD_SPEC.md`](BUILD_SPEC.md)
- Agent setup and run instructions: [`agent/README.md`](agent/README.md)

## Status

Phase 1 (agent joins a room and transcribes speakers) is scaffolded, the
worker connects to LiveKit successfully, and a real `OPENAI_API_KEY` is now
in place — ready to verify Phase 1 acceptance (live transcripts from a real
meeting). See `agent/README.md` and `BUILD_SPEC.md` §3 for details, including
why Groq was considered and ruled out as a substitute provider.
