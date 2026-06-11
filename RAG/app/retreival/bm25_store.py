import pickle

from rank_bm25 import BM25Okapi


class BM25Store:

    def __init__(self, docs):

        self.docs = docs

        self.model = BM25Okapi(
            [
                d.page_content.split()
                for d in docs
            ]
        )

    def search(
        self,
        query,
        k=20
    ):

        scores = (
            self.model.get_scores(
                query.split()
            )
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            idx
            for idx, _
            in ranked[:k]
        ]

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str):
        with open(path, "rb") as f:
            return pickle.load(f)