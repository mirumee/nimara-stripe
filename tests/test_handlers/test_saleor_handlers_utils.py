import pytest

from nimara_stripe.api.saleor.utils import build_url
from nimara_stripe.settings import settings

pytestmark = pytest.mark.anyio


async def test_build_url_if_debug_is_true():
    url = build_url("example.com", "/saleor/app")

    assert url == "https://example.com/nimara-stripe/saleor/app"


async def test_build_url_if_debug_is_false(monkeypatch):
    monkeypatch.setattr(settings, "debug", False)
    url = build_url("example.com", "/saleor/app")

    assert url == "https://example.com/saleor/app"

    monkeypatch.undo()
