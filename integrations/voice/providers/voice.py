# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
#

import requests
requests.packages.urllib3.disable_warnings()

class VoiceException(Exception):
    pass


class Voice():
    def __init__(self, voice_config, audio_file, source_id):
        self.audio_file = audio_file
        self.source_id = source_id
        self.config = self._check_config(voice_config)

    def transcribe(self):
        url = self._build_url()
        headers = self._build_headers()

        with open(self.audio_file, 'rb') as f:
            response = requests.post(url, data=f, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                raise VoiceException(response.text)

    def _build_headers(self):
        '''create the headers required by Nuance'''
        headers = dict()
        headers['Accept'] = 'text/plain'
        headers['Accept-Language'] = 'eng-USA'
        headers['Accept-Topic'] = 'Dictation'
        headers['Content-Type'] = self._build_content_type()
        headers['X-Dictation-NBestListSize'] = 1
        return headers


    def _build_url(self):
        '''create the Nuance url'''
        return 'https://{}?appId={}&appKey={}&id={}'.format(self.config.url, self.config.app_id, self.config.app_key, self.source_id)

    def _build_content_type(self):
        '''get audio file params, or raise exception on error'''
        import wave
        w = wave.open(self.audio_file, 'rb')
        framerate = w.getframerate()
        bits = w.getsampwidth() * 8
        w.close()
        return 'audio/x-wav;codec=pcm;bit={};rate={}'.format(bits, framerate)

    def _check_config(self, config):
        '''validate the config values'''
        if config.url is None:
            raise VoiceException('No URL supplied')

        if config.app_id is None:
            raise VoiceException('No appId supplied')

        if config.app_key is None:
            raise VoiceException('No appKey supplied')

        return config


class VoiceConfig():
    SECTION = 'voice'

    def __init__(self, url, app_id, app_key):
        self.url = url
        self.app_id = app_id
        self.app_key = app_key

    @classmethod
    def from_config_file(cls, config):
        from ConfigParser import Error

        url = None
        app_id = None
        app_key = None

        try:
            url = config.get(VoiceConfig.SECTION, 'asrUrl')
            app_id = config.get(VoiceConfig.SECTION, 'appId')
            app_key = config.get(VoiceConfig.SECTION, 'appKey')
        except Error, e:
            pass

        return VoiceConfig(url, app_id, app_key)
