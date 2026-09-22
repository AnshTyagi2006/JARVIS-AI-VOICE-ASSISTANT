from jarvis.services.web_service import WebService


def test_web_service_can_be_created():
    web = WebService()

    assert web is not None


def test_sports_query_detection():
    web = WebService()

    assert web._is_sports_query(
        "what was rohit sharma latest score"
    )


def test_general_query_is_not_sports():
    web = WebService()

    assert not web._is_sports_query(
        "what is machine learning"
    )
    