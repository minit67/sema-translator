import os

AGENT_IDENTITY = "translator-agent"
AGENT_NAME = os.getenv("AGENT_NAME", "translator-agent")

# Fixed per BUILD_SPEC.md; used from Phase 3 onward for TTS fan-out.
TARGET_LANGS = ["te", "en", "hi", "es"]
