from jarvis.services.weather_service import WeatherService


def test_weather_service_can_be_created():
    weather = WeatherService()

    assert weather is not None