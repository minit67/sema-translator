# sema-interpreter

Standalone home for the **Sema Interpreter agent** (Python) used by Zoiko
Sema's parallel AI voice translation feature. This repo holds only the agent
— the client and server live in the separate Zoiko Sema repo.

- Canonical naming, UI, and identity spec: [`docs/naming_spec.md`](docs/naming_spec.md)
- Full plan and phase breakdown: [`BUILD_SPEC.md`](BUILD_SPEC.md)
- Agent setup and run instructions: [`agent/README.md`](agent/README.md)

## Status

Phase 1 (agent joins a room and transcribes speakers) is verified. Phase 2
(translate a final segment and speak it back on one hard-coded language) is
coded and the OpenAI key quota issue is resolved, but the Phase 2 live
acceptance test still has not passed: live testing on 2026-07-14 found the
audio reaching the agent was distorted, traced to a real connection-quality
drop and latency spike in the LiveKit session itself (confirmed in LiveKit's
own dashboard), not the agent code, microphone, or OpenAI. See
`BUILD_SPEC.md` §3 for the LiveKit Cloud vs self-hosted discrepancy also
found that day. Groq and NVIDIA Riva were considered as cheaper/free
alternatives and ruled out: neither covers the full Hindi/Spanish/Telugu
target set. See `agent/README.md` and `BUILD_SPEC.md` §3 for details.
