from sentence_transformers import (
    CrossEncoder
)


class BGEReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-large"
        )

    def rerank(
        self,
        query,
        docs,
        top_k=5
    ):

        pairs = [
            (
                query,
                doc.page_content
            )
            for doc in docs
        ]

        scores = (
            self.model.predict(
                pairs
            )
        )

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, _
            in ranked[:top_k]
        ]