import os
import sys
import json
import requests
import urllib.parse


funcs = {'commande': {}, 'action': {}}

class Cmd(str):
    '''
        Object for text of message
    '''
    __atts = []

    def __init__(self, text):
        str.__init__(text)

    def set_atts(self, atts):
        for att in atts:
            self.__atts.append(att)

    @property
    def attachments(self):
        return self.__atts


class Payload:
    '''
        Object for Payload Management
    '''
    def __init__(self, payload, **kwargs) -> None:
        '''
            Object for Payload Management
        '''
        self.payload = payload
        self.data = kwargs

    def __str__(self):
        return self.payload

    @staticmethod
    def trt_payload_in(payload):
        """
        processing of payloads received in a sequence of structured parameters
        
        @params: payload [String]
        @return: payload [String] , structured parameters Dict
        """

        payload = urllib.parse.unquote(str(payload))

        res = {}
        while '{{' in payload:
            start = payload.index('{{')
            end = payload.index('}}')
            items = payload[start+2:end].split('===')
            res[items[0]] = items[1]
            payload = payload.replace(payload[start:end+2], '')
        return payload.strip(), res

    @staticmethod
    def trt_payload_out(payload):
        """
        Processing of a Payload type as a character string
        
        @params: payload [ Payload | String ]
        @return: String
        """
        if isinstance(payload, Payload):
            tmp = ''
            for key_data, val_data in payload.data.items():
                tmp += f'{{{{{key_data}==={val_data}}}}} '
            return urllib.parse.quote(payload.payload + ' ' + tmp)
        return urllib.parse.quote(payload)


def analyse(data):
    '''
        Function analyzing data received from Facebook
        The data received are of type Json .
    '''
    def struct_atts(data):
        return data['payload']['url']

    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # Get user_id
                sender_id = message['sender']['id']
                if message['message'].get('attachments'):
                    # Get file name
                    data = message['message'].get('attachments')
                    # creation de l'objet cmd personalisé
                    atts = list(map(struct_atts, data))
                    cmd = Cmd(atts[0])
                    cmd.set_atts(atts)
                    return sender_id, cmd, message
                elif message['message'].get('quick_reply'):
                    # if the response is a quick reply
                    return  sender_id, Cmd(message['message']['quick_reply'].get('payload')), message
                elif message['message'].get('text'):
                    # if the response is a simple text
                    return  sender_id, Cmd(message['message'].get('text')), message
            if message.get('postback'):
                recipient_id = message['sender']['id']
                pst_payload = message['postback']['payload']
                return recipient_id, Cmd(pst_payload), message


def command(*args, **kwargs):
    """
        A decorator that registers the function as the route 
            of a processing per command sent.
    """
    def call_fn(function):
        funcs['commande'][args[0]] = function
    return call_fn


def action(*args, **kwargs):
    """
        A decorator that registers the function as the route
            of a defined action handler.
    """
    def call_fn(function):
        funcs['action'][args[0]] = function
    return call_fn


def download_file(url, file):
    '''
        Downloading a file from an url.
        
        Args:
            url: direct link for the attachment

            file: filename with path
    '''
    res = requests.get(url, allow_redirects=True)

    with open(file, 'wb') as f:
        f.write(res.content)

    return file

def translate(key, lang):
    '''
        translate a keyword or sentence

        @params:
        
            key: the key used in langs.json file 
            
            lang: the langage code in format fr, en, mg, ...

        this function uses the langs.json file.
    '''
    if not lang:
        return key

    if not os.path.isfile("langs.json"):
        print(
            "Warning! langs.json not found",
            file=sys.stderr
        )
        from .source import langs
        with open("langs.json", "w") as fichier:
            fichier.write(langs)
            print('langs.json created!')
        return key

    with open("langs.json") as fichier:
        trans = json.load(fichier)

    keyword = trans.get(key)

    if keyword:
        if keyword.get(lang):
            return keyword.get(lang)
    return key


def simulate(message, user, conf, **params):
    '''
        Simulate a message send by an user
    '''
    data_json = {
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "message":
                            {
                                "text": mes,
                            },
                        "sender":
                            {
                                "id": user
                            }
                    }
                ]
            }
        ]
    }
    header = {'content-type': 'application/json; charset=utf-8'}
    return requests.post(
        f'http://127.0.0.1:{conf.APP_PORT}',
        json=data_json,
        headers=header,
        params=params
    )