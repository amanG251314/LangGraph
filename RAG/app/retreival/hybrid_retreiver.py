from app.retreival.rrf import (
    reciprocal_rank_fusion
)


class HybridRetriever:

    def __init__(
        self,
        bm25,
        faiss,
        docs
    ):

        self.bm25 = bm25
        self.faiss = faiss
        self.docs = docs

    def retrieve(
        self,
        query,
        k=10
    ):

        bm25_ids = (
            self.bm25.search(query)
        )

        dense_ids = (
            self.faiss.search(query)
        )

        fused = (
            reciprocal_rank_fusion(
                bm25_ids,
                dense_ids
            )
        )

        return [
            self.docs[i]
            for i in fused[:k]
        ]