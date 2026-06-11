from functools import partial

from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import retrieve_node, build_context_node, generate_node


def build_graph(retriever, checkpointer):

    builder = StateGraph(AgentState)

    builder.add_node(
        "retrieve",
        partial(retrieve_node, retriever=retriever)
    )
    builder.add_node("build_context", build_context_node)
    builder.add_node("generate", generate_node)

    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "build_context")
    builder.add_edge("build_context", "generate")
    builder.add_edge("generate", END)

    return builder.compile(checkpointer=checkpointer)
