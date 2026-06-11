from collections import defaultdict


def reciprocal_rank_fusion(
    bm25_results,
    dense_results,
    k=60
):

    scores = defaultdict(float)

    for rank, doc_id in enumerate(
        bm25_results
    ):
        scores[doc_id] += (
            1 / (k + rank + 1)
        )

    for rank, doc_id in enumerate(
        dense_results
    ):
        scores[doc_id] += (
            1 / (k + rank + 1)
        )

    return sorted(
        scores.keys(),
        key=lambda x: scores[x],
        reverse=True
    )