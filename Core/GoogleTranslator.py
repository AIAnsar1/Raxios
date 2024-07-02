import json
import random

import requests

import Config.Conf

from urllib.parse import quote


class GoogleTranslator():

    '''
    :param
    :type
    '''

    def __init__(self, UrlSuffix="com", TimeOut=5, Proxies=None):
        self.proxies = Proxies
        if UrlSuffix not in Config.Conf.URLS_SUFFIX:
            self.UrlSuffix = Config.Conf.URLS_SUFFIX_DEFAULT
        else:
            self.UrlSuffix = UrlSuffix
        UrlBase = "https://translate.google.{}".format(self.UrlSuffix)
        self.url = UrlBase + "/_/TranslateWebserverUi/data/batchexecute"
        self.Timeout = TimeOut



    def __PackageRPC(self, text, LangSrc='auto', LangTgT='auto'):
        GOOGLE_TTS_RPC = ["MkEWBc"]
        Parameter = [[text.strip(), LangSrc, LangTgT, True], [1]]
        EscapedParameter = json.dumps(Parameter, separators=(',', ':'))
        Rpc = [[[random.choice(GOOGLE_TTS_RPC), EscapedParameter, None, "generic"]]]
        EscapedRpc = json.dumps(Rpc, separators=(',', ':'))
        # TextUrlDecode = quote(text.strip())
        FreqInitial = "f.req={}&".format(quote(EscapedRpc))
        Freq = FreqInitial
        return Freq


    def Translate(self, text, LangTgT='auto', LangSrc='auto', Pronounce=False):
        try:
            Lang = Config.Conf.LEANGUAGES[LangSrc]
        except:
            LangSrc = 'auto'
        try:
            Lang = Config.Conf.LEANGUAGES[LangTgT]
        except:
            LangSrc = 'auto'

        text = str(text)
        if len(text) >= 5000:
            return " [ WARNING ]: Can Only Detect Less Than 5000 Characters!"
        if len(text) == 0:
            return ""
        Headers = {
            "Referer": "http://translate.google.{}/".format(self.UrlSuffix),
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        Freq = self.__PackageRPC(text, LangSrc, LangTgT)
        Response = requests.Request(method='POST', url=self.url, data=Freq, headers=Headers)

        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.session() as S:
                S.proxies = self.proxies
                R = S.send(request=Response.prepare(), verify=False, timeout=self.Timeout)
                for Line in R.iter_lines(chunk_size=1024):
                    DeCodedLine = Line.decoce('UTF-8')
                    if "MkEWBc" in DeCodedLine:
                        try:
                            Response = (DeCodedLine)
                            Response = json.loads(Response)
                            Response = list(Response)
                            Response = json.loads(Response[0][2])
                            response_ = list(Response)
                            Response = response_[1][0]
                            if len(Response) == 1:
                                if len(Response[0]) > 5:
                                    Sentences = Response[0][5]
                                else:
                                    Sentences = Response[0][0]
                                    if Pronounce == False:
                                        return Sentences
                                    elif Pronounce == True:
                                        return [Sentences, None, None]
                                TranslateText = ""
                                for sentences in Sentences:
                                    Sentences = Sentences[0]
                                    if isinstance(Sentences, str):
                                        TranslateText += Sentences.strip() + " "
                                TranslateText = TranslateText
                                if Pronounce == False:
                                    return TranslateText
                                elif Pronounce == True:
                                    PronounceSrc = (response_[0][0])
                                    PronounceTgT = (response_[1][0][0][1])
                                    return [TranslateText, PronounceSrc, PronounceTgT]
                            elif len(Response) == 2:
                                Sentences = []
                                for i in Response:
                                    Sentences.append(i[0])
                                if Pronounce == False:
                                    return Sentences
                                elif Pronounce == True:
                                   PronounceSrc = (response_[0][0])
                                   PronounceTgT = (response_[1][0][0][1])
                                   return [TranslateText, PronounceSrc, PronounceTgT]
                        except Exception as E:
                            raise E
                R.raise_for_status()
        except requests.exceptions.HTTPError as E:
            raise GoogleTranslator(TTS=self, Response=R)
        except requests.exceptions.RequestException as E:
            raise GoogleTranslator(TTS=self)



    def Detect(self, text):
        text = str(text)
        if len(text) >= 5000:
            return Config.Conf.ConfigLog.debug(" [ WARNING ]: Can Only Detect Less Than 5000 Characters!")
        if len(text) == 0:
            return ""
        Headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        Freq = self.__PackageRPC(text)
        Response = requests.Request(method='POST', url=self.url, data=Freq, headers=Headers)

        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.session() as S:
                S.proxies = self.proxies
                R = S.send(request=Response.prepare(), verify=False, timeout=self.Timeout)
                for Line in R.iter_lines(chunk_size=1024):
                    DeCodedLine = Line.decoce('UTF-8')
                    if "MkEWBc" in DeCodedLine:
                        try:
                            Response = (DeCodedLine)
                            Response = json.loads(Response)
                            Response = list(Response)
                            Response = json.loads(Response[0][2])
                            Response = list(Response)
                            DetectLang = Response[1][0]
                        except Exception:
                            raise Exception
                        return [DetectLang, Config.Conf.LEANGUAGES[DetectLang.lower()]]
                    R.raise_for_status()
        except requests.exceptions.HTTPError as E:
            Config.Conf.ConfigLog.debug(str(E))
            raise GoogleTranslator(TTS=self, Response=R)
        except requests.exceptions.RequestException as E:
            Config.Conf.ConfigLog.debug(str(E))
            raise GoogleTranslator(TTS=self)

































