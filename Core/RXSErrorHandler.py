
class RXSErrorHandler(Exception):
    def __init__(self, Msg=None, **Kwargs):
        self.tts = Kwargs.pop('tts', None)
        self.rsp = Kwargs.pop('response', None)

        if Msg:
            self.msg = Msg
        elif self.tts is not None:
            self.msg = self.InterMsg(self.tts, self.rsp)
        else:
            self.msg = None
        super(RXSErrorHandler, self).__init__(self.msg)

    def InterMsg(self, tts, rsp=None):
        cause = "unknown"

        if rsp is None:
            premise = "Failed to Connect"
            return "{} Probable Cause: {}".format(premise, "Timeout")
        else:
            status = rsp.StatusCode
            reason = rsp.reason
            premise = "{:d} ({}) From TTS API".format(status, reason)

            if status == 403:
                cause = "Bad Token or UpStream API Changes"
            elif status == 200 and not tts.LangCheck:
                cause = "No Audio Stream in Response Unsupported Language '%s'" % self.tts.lang
            elif status >= 500:
                cause = "UpStream API Error Try Again Later"
        return "{}, Probable Cause {}".format(premise, cause)
