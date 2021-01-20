

import json
import base64
import logging
import os
from urllib import request, parse

class BaiduVoiceHttpClient():
    logger = logging.getLogger(__name__)
    apiKey = ""
    secretKey = ""

    def __init__(self, apiKey, secretKey):
        self.apiKey = apiKey
        self.secretKey = secretKey

    def __getToken(self):
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (self.apiKey, self.secretKey)
        response = self.__request(auth_url, '')
        return response['access_token']

    def VocieTranslation(self, Language, Channel, audioFile, Format, Rate):

        Token = self.__getToken()
        cuid = Token[Token.index("-") + 1:]
        API_url = "http://vop.baidu.com/server_api"

        audioFileLen = os.path.getsize(audioFile)
        with open(audioFile, 'rb') as fout:
            base_data = base64.b64encode(fout.read())
        base_data = parse.unquote(base_data.decode("utf-8"), "utf-8")
        Postdata = {'format': Format, 'rate': Rate, 'channel': Channel, 'lan': Language,
                    'token': Token, 'cuid': cuid, 'len': audioFileLen, 'speech': base_data}
        try:
            data = json.dumps(Postdata).encode('utf8')
            req = request.Request(API_url, data=data, headers={"content-type": "application/json"})
            result = request.urlopen(req, timeout=2)
            response = result.read()
            response = response.decode("utf-8")
            response = json.loads(response)
        except Exception as e:
            self.logger.error(e)
        if (response['err_no'] == 0):
            return response['result'][0]
        else:
            return response['err_msg']

    def __request(self, url, data):
        try:
            data = parse.urlencode(data).encode("utf-8")
            req = request.Request(url, data=data)
            res = request.urlopen(req)
            response = res.read()
            response = response.decode("utf-8")
            json_data = json.loads(response)
            return json_data
        except Exception as e:
            self.logger.error(e)

