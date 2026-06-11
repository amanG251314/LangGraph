from typing import Annotated
from typing import TypedDict

from langgraph.graph.message import add_messages


class ChatState(TypedDict):

    messages: Annotated[list, add_messages]

    user_id: str

    session_id: str