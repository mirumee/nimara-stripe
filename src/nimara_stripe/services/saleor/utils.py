from collections import namedtuple
from urllib.parse import urlsplit, urlunsplit

SaleorURLParts = namedtuple("SaleorURLParts", ["url", "domain"])


def get_saleor_url_parts(saleor_api_url: str) -> SaleorURLParts:
    saleor_url_parts = urlsplit(saleor_api_url)
    saleor_url_parts = saleor_url_parts._replace(path="")
    saleor_url = urlunsplit(saleor_url_parts)
    saleor_url_parts = saleor_url_parts._replace(scheme="")
    saleor_domain = saleor_url_parts.netloc

    return SaleorURLParts(saleor_url, saleor_domain)
