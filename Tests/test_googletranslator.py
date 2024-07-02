import pytest
import json
import random

from unittest.mock import MagicMock
from unittest.mock import patch
from Core import GoogleTranslator



@pytest.fixture()
def translator():
    return GoogleTranslator(UrlSuffix='com', Timeout=5, Proxies=None)




@patch('requests.Session.send')
def test_translate(mock_send, translator):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [
        json.dumps([
            [["MkEWBc", "[[\"Hello\",\"en\",\"en\",true]]", None, "generic"]],
            None, "[[\"Hello\"]]", None, None
        ]).encode('utf-8')
    ]
    mock_send.return_value = mock_response
    result = translator.Translate("Hello", LangTgT='ru')
    assert result == "Hello "

@patch('requests.Session.send')
def test_detect(mock_send, translator):
    # Мокируем ответ от Google Translate
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [
        json.dumps([
            [["MkEWBc", "[[\"Hello\",\"en\",\"en\",true]]", None, "generic"]],
            None, "[[\"Hello\"]]", None, None
        ]).encode('utf-8')
    ]
    mock_send.return_value = mock_response
    result = translator.Detect("Hello")
    assert result == ['en', 'English']

def test_init_default_url_suffix():
    translator = GoogleTranslator()
    assert translator.UrlSuffix == 'com'
    assert translator.url == "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute"

def test_init_custom_url_suffix():
    translator = GoogleTranslator(UrlSuffix='ru')
    assert translator.UrlSuffix == 'ru'
    assert translator.url == "https://translate.google.ru/_/TranslateWebserverUi/data/batchexecute"

def test_init_invalid_url_suffix():
    translator = GoogleTranslator(UrlSuffix='invalid')
    assert translator.UrlSuffix == 'com'
    assert translator.url == "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute"