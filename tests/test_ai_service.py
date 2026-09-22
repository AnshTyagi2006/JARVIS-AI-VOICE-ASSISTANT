from jarvis.services.ai_service import AIService


def test_ai_service_can_be_created():
    ai = AIService()

    assert ai is not None