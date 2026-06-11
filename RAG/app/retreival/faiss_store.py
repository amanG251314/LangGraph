import faiss
import numpy as np


class FaissStore:

    def __init__(
        self,
        embeddings,
        documents
    ):

        self.embeddings = embeddings
        self.documents = documents

        vectors = (
            embeddings.embed_documents(
                [
                    d.page_content
                    for d in documents
                ]
            )
        )

        dim = len(vectors[0])

        self.index = (
            faiss.IndexHNSWFlat(
                dim,
                32
            )
        )

        self.index.add(
            np.array(
                vectors,
                dtype="float32"
            )
        )

    def search(
        self,
        query,
        k=20
    ):

        vector = (
            self.embeddings.embed_query(
                query
            )
        )

        scores, indices = (
            self.index.search(
                np.array(
                    [vector],
                    dtype="float32"
                ),
                k
            )
        )

        return [int(i) for i in indices[0] if i != -1]

    def save(self, index_path: str):
        faiss.write_index(self.index, index_path)

    @classmethod
    def load(cls, embeddings, documents, index_path: str):
        instance = cls.__new__(cls)
        instance.embeddings = embeddings
        instance.documents = documents
        instance.index = faiss.read_index(index_path)
        return instance