class ChatService:

    def __init__(self, graph):

        self.graph = graph

    def _config(
        self,
        session_id: str
    ):

        return {
            "configurable": {
                "thread_id": session_id
            }
        }

    def chat(
        self,
        user_id: str,
        session_id: str,
        message: str
    ):

        result = self.graph.invoke(
            {
                "messages": [
                    (
                        "user",
                        message
                    )
                ],
                "user_id": user_id,
                "session_id": session_id
            },
            config=self._config(
                session_id
            )
        )

        return (
            result["messages"][-1]
            .content
        )

    def get_history(
        self,
        session_id: str
    ):

        snapshot = (
            self.graph.get_state(
                self._config(session_id)
            )
        )

        return snapshot.values

    def clear_thread(
        self,
        session_id: str
    ):

        # For postgres checkpointer
        # typically handled by deleting
        # checkpoints directly

        print(
            f"Clear session: {session_id}"
        )