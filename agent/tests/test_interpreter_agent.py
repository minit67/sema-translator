import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import interpreter_agent as agent


@pytest.mark.parametrize(
    "identity,expected",
    [
        ("sema-interpreter-agent", True),
        ("sema-interpreter-worker-2", True),
        ("translator-agent", True),
        ("u:398", False),
        ("guest-42", False),
    ],
)
def test_is_agent(identity, expected):
    participant = SimpleNamespace(identity=identity)
    assert agent.is_agent(participant) is expected


@pytest.mark.asyncio
async def test_translate_text_returns_stripped_content():
    fake_response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="  hello  "))]
    )
    with patch.object(
        agent.translate_client.chat.completions, "create", AsyncMock(return_value=fake_response)
    ):
        result = await agent.translate_text("hola", "es", "en")
    assert result == "hello"


@pytest.mark.asyncio
async def test_translate_and_speak_skips_same_language():
    audio_source = SimpleNamespace()
    participant = SimpleNamespace(identity="u:398")
    with patch.object(agent, "translate_text", AsyncMock()) as translate_mock:
        await agent.translate_and_speak(participant, "hello", agent.PHASE2_TARGET_LANG, audio_source)
    translate_mock.assert_not_called()


@pytest.mark.asyncio
async def test_translate_and_speak_retries_once_then_gives_up():
    audio_source = SimpleNamespace()
    participant = SimpleNamespace(identity="u:398")
    with (
        patch.object(agent, "translate_text", AsyncMock(side_effect=RuntimeError("boom"))) as translate_mock,
        patch.object(agent, "speak_translation", AsyncMock()) as speak_mock,
    ):
        await agent.translate_and_speak(participant, "hola", "es", audio_source)
    assert translate_mock.call_count == 2
    speak_mock.assert_not_called()
