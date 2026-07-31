import os

import pytest
from bindai_model import Model

pytestmark = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not configured.",
)


def test_openai_provider_registered():

    model = Model(
        "openai",
    )

    assert model.provider is not None
