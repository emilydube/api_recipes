# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
#

import requests
from json import dumps, loads


class ReceptivitiException(Exception):
    pass


class Content():
    NOTSPECIFIED = 0
    MALE = 1
    FEMALE = 2

    PERSONAL_WRITING = 1
    PERSONAL_EMAIL_CORRESPONDENCE = 2
    PROFESSIONAL_CORRESPONDENCE = 3
    SOCIAL_MEDIA = 4
    COMMERCIAL_WRITING = 5
    PROFESSIONAL_OR_SCIENTIFIC_WRITING = 6
    ANONYMOUS_REVIEW = 7
    OTHER = 0

    URL = 'https://app.receptiviti.com/v2/api/person'

    def __init__(self, config, name, gender, person_handle, content_handle, content_source, language, language_content):
        self.content = {
            'content_handle': content_handle,
            'content_source': content_source,
            'language': language,
            'language_content': language_content
        }

        self.person = {
            'name': name,
            'gender': gender,
            'person_handle': person_handle,

        }

        self.config = self._check_config(config)


    def analyse(self):
        headers = self._build_headers()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'

        # Create person and content if this person does not yet exist in the database, else create content for the existing user
        data = dict()
        person_id = self.get_person_id(self.person['person_handle'])
        if person_id is not None:
            url = '{}/{}/contents'.format(Content.URL, person_id)  # url to create content for an existing user
            data = self.content  # only send content information
        else:
            url = Content.URL  # url to create person and content
            data = self.person
            data['content'] = self.content  # content information is embedded in person dictionary

        response = requests.post(url, headers=headers, data=dumps(data))  # submit the content

        if response.status_code == 200:
            if person_id is None:
                person = response.json()
                person_id = person['_id']
            profile = self.get_profile(person_id)
            return profile
        else:
            raise ReceptivitiException(response.content)


    def get_profile(self, person_id):
        headers = self._build_headers()
        response = requests.get('{}/{}/profile'.format(Content.URL, person_id), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise ReceptivitiException(response.content)


    def get_person_id(self, person_handle):
        headers = self._build_headers()
        params = { 'person_handle': person_handle}
        response = requests.get(Content.URL, headers=headers, params=params)
        if response.status_code == 200:
            matches = response.json()
            if len(matches) > 0:
                return matches[0]['_id']

            return None
        else:
            raise ReceptivitiException(response.content)


    def _build_headers(self):
        '''create the headers required by Receptiviti'''
        headers = dict()
        headers['X-API-KEY'] = self.config.api_key
        headers['X-API-SECRET-KEY'] = self.config.api_secret
        return headers

    def _check_config(self, config):
        '''validate the config values'''
        if config.api_key is None:
            raise ReceptivitiException('No api_key supplied')

        if config.api_secret is None:
            raise ReceptivitiException('No api_secret supplied')

        return config


class ReceptivitiConfig():
    SECTION = 'receptiviti'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    @classmethod
    def from_config_file(cls, config):
        from ConfigParser import Error

        api_key = None
        api_secret = None

        try:
            api_key = config.get(ReceptivitiConfig.SECTION, 'api_key')
            api_secret = config.get(ReceptivitiConfig.SECTION, 'api_secret')
        except Error, e:
            pass

        return ReceptivitiConfig(api_key, api_secret)
