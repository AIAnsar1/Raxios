import pytest

from unittest.mock import MagicMock
from Core import RXSErrorHandler


def test_rxserrorhandler_with_msg():
    # Проверяем, что исключение корректно передает сообщение, если оно указано
    err = RXSErrorHandler(Msg="Test error message")

    assert str(err) == "Test error message"


def test_rxserrorhandler_with_tts_no_response():
    # Проверяем, что исключение корректно формирует сообщение на основе tts, если rsp не указан
    tts_mock = MagicMock()
    err = RXSErrorHandler(tts=tts_mock)
    assert str(err) == "Failed to Connect Probable Cause: Timeout"


def test_rxserrorhandler_with_response_status_403():
    # Проверяем, что исключение корректно формирует сообщение на основе rsp со статусом 403
    tts_mock = MagicMock()
    rsp_mock = MagicMock()
    rsp_mock.StatusCode = 403
    rsp_mock.reason = "Forbidden"

    err = RXSErrorHandler(tts=tts_mock, response=rsp_mock)
    assert str(err) == "403 (Forbidden) From TTS API, Probable Cause Bad Token or UpStream API Changes"


def test_rxserrorhandler_with_response_status_200_no_langcheck():
    # Проверяем, что исключение корректно формирует сообщение на основе rsp со статусом 200 и отсутствием LangCheck
    tts_mock = MagicMock()
    tts_mock.LangCheck = False
    tts_mock.lang = "en"
    rsp_mock = MagicMock()
    rsp_mock.StatusCode = 200
    rsp_mock.reason = "OK"

    err = RXSErrorHandler(tts=tts_mock, response=rsp_mock)
    assert str(err) == "200 (OK) From TTS API, Probable Cause No Audio Stream in Response Unsupported Language 'en'"


def test_rxserrorhandler_with_response_status_500():
    # Проверяем, что исключение корректно формирует сообщение на основе rsp со статусом 500
    tts_mock = MagicMock()
    rsp_mock = MagicMock()
    rsp_mock.StatusCode = 500
    rsp_mock.reason = "Internal Server Error"

    err = RXSErrorHandler(tts=tts_mock, response=rsp_mock)
    assert str(err) == "500 (Internal Server Error) From TTS API, Probable Cause UpStream API Error Try Again Later"


def test_rxserrorhandler_no_msg_no_tts():
    # Проверяем, что исключение корректно формируется, если ни Msg, ни tts не указаны
    err = RXSErrorHandler()
    assert str(err) == "None"















