import os

AGENT_IDENTITY = "sema-interpreter-agent"
AGENT_NAME = os.getenv("AGENT_NAME", "sema-interpreter-agent")

# Fixed per BUILD_SPEC.md; used from Phase 3 onward for TTS fan-out.
TARGET_LANGS = ["te", "en", "hi", "es"]

# Phase 2 (BUILD_SPEC.md §6): prove the loop with one hard-coded target
# language before fanning out to TARGET_LANGS in Phase 3.
PHASE2_TARGET_LANG = "en"
