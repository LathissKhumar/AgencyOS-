import socket
from unittest.mock import patch

import pytest

from leadfinder.crawler.url_validator import SSRFSecurityError, UrlSecurityValidator


def _fake_addr_info(ip: str):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 0))]


def test_valid_public_urls():
    validator = UrlSecurityValidator()
    # Pin DNS resolution: live lookups are environment-dependent (proxies,
    # NAT64 gateways) and would make the SSRF check block valid hostnames.
    with patch(
        "socket.getaddrinfo", return_value=_fake_addr_info("93.184.216.34")
    ):
        assert (
            validator.validate_url("https://example.com/page")
            == "https://example.com/page"
        )
        assert (
            validator.validate_url("http://books.toscrape.com")
            == "http://books.toscrape.com"
        )
        assert (
            validator.validate_url("https://www.flipkart.com/product")
            == "https://www.flipkart.com/product"
        )


def test_block_invalid_schemes():
    validator = UrlSecurityValidator()
    with pytest.raises(SSRFSecurityError, match="Invalid URL scheme"):
        validator.validate_url("ftp://example.com/file")
    with pytest.raises(SSRFSecurityError, match="Invalid URL scheme"):
        validator.validate_url("file:///etc/passwd")
    with pytest.raises(SSRFSecurityError, match="Invalid URL scheme"):
        validator.validate_url("javascript:alert(1)")


def test_block_private_ips_and_loopback():
    validator = UrlSecurityValidator()
    with pytest.raises(
        SSRFSecurityError, match="Private, loopback, or cloud metadata IP blocked"
    ):
        validator.validate_url("http://127.0.0.1:8000/secret")
    with pytest.raises(
        SSRFSecurityError, match="Private, loopback, or cloud metadata IP blocked"
    ):
        validator.validate_url("http://localhost:8080")
    with pytest.raises(
        SSRFSecurityError, match="Private, loopback, or cloud metadata IP blocked"
    ):
        validator.validate_url("http://169.254.169.254/latest/meta-data")
    with pytest.raises(
        SSRFSecurityError, match="Private, loopback, or cloud metadata IP blocked"
    ):
        validator.validate_url("http://10.0.0.1/admin")
    with pytest.raises(
        SSRFSecurityError, match="Private, loopback, or cloud metadata IP blocked"
    ):
        validator.validate_url("http://192.168.1.1/router")


def test_allow_private_when_explicitly_configured():
    validator = UrlSecurityValidator(allow_private=True)
    assert (
        validator.validate_url("http://127.0.0.1:8000/test")
        == "http://127.0.0.1:8000/test"
    )
    assert validator.validate_url("http://localhost:8000") == "http://localhost:8000"
