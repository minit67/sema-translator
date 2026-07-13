import os

AGENT_IDENTITY = "sema-interpreter-agent"
AGENT_NAME = os.getenv("AGENT_NAME", "sema-interpreter-agent")

# Fixed per BUILD_SPEC.md; used from Phase 3 onward for TTS fan-out.
TARGET_LANGS = ["te", "en", "hi", "es"]
