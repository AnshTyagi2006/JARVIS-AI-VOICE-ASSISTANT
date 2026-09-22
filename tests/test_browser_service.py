from jarvis.services.browser_service import BrowserService


def test_supported_website_exists():
    browser = BrowserService()

    assert "youtube" in browser.WEBSITES
    assert "google" in browser.WEBSITES


def test_open_unsupported_website_returns_false():
    browser = BrowserService()

    assert browser.open_website("not-a-real-site") is False
    