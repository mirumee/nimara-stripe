import pytest

from nimara_stripe.api.saleor.utils import build_url

pytestmark = pytest.mark.anyio


async def test_build_url():
    url = build_url("example.com", "/saleor/app")

    assert url == "https://example.com/saleor/app"
