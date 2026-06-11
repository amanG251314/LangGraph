from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.graph.state import (
    ChatState
)

from app.graph.nodes import (
    chatbot_node
)

# utility class with static factory method to build the graph
class GraphBuilder:

    @staticmethod
    def build(checkpointer):

        builder = StateGraph(
            ChatState
        )

        builder.add_node(
            "chatbot",
            chatbot_node
        )

        builder.add_edge(
            START,
            "chatbot"
        )

        builder.add_edge(
            "chatbot",
            END
        )

        return builder.compile(
            checkpointer=checkpointer
        )