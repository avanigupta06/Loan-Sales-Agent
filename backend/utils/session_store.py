"""In-memory session store for conversation state management."""

from models.schemas import ConversationState
from typing import Dict

_sessions: Dict[str, ConversationState] = {}


def get_session(session_id: str) -> ConversationState:
    if session_id not in _sessions:
        _sessions[session_id] = ConversationState(session_id=session_id)
    return _sessions[session_id]


def save_session(state: ConversationState) -> None:
    _sessions[state.session_id] = state


def delete_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def get_all_sessions() -> Dict[str, ConversationState]:
    return _sessions
