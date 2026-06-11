from langchain_core.messages import SystemMessage

from app.prompts.rag_prompts import (
    RAG_PROMPT
)

from app.llm.llm_factory import (
    get_llm
)

llm = get_llm()

def retrieve_node(
    state,
    retriever
):

    query = (
        state["messages"][-1].content
    )

    docs = retriever.retrieve(query)

    return {
        "retrieved_docs": docs
    }

def build_context_node(state):

    context = "\n\n".join(
        [
            doc.page_content
            for doc in state[
                "retrieved_docs"
            ]
        ]
        )

    return {
        "context": context
    }

def generate_node(state):

    system = SystemMessage(
        content=RAG_PROMPT.format(
            context=state["context"]
        )
    )

    response = llm.invoke(
        [system] + state["messages"]
    )

    return {
        "messages": [response],
        "answer": response.content
    }