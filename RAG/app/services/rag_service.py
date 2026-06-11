class RAGService:

    def __init__(
        self,
        graph
    ):

        self.graph = graph

    def chat(
        self,
        query,
        thread_id
    ):

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = self.graph.invoke(
            {
                "messages": [
                    (
                        "user",
                        query
                    )
                ]
            },
            config=config
        )

        return result["answer"]