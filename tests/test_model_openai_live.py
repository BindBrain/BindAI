import os

import pytest

from bindai_model import Model


pytestmark = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not configured.",
)


def test_openai_live():

    model = Model(
        "openai",
    )

    result = model.generate(
        "Reply with exactly: hello",
    )

    assert "hello" in result.content.lower()