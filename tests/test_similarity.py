from bindai_knowledge.similarity import cosine_similarity


def test_cosine_similarity():

    score = cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    )

    assert score == 1.0


def test_cosine_similarity_different():

    score = cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )

    assert score == 0.0