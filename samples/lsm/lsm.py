#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
# Author: Abdul Gani
#
#
import requests
import json


def v(verbose, text):
    if verbose:
        print text

class Receptiviti():
    def __init__(self, server, api_key, api_secret, verbose=False):
        """
        initialise a Receptiviti object

        :type server: str
        :type api_key: str
        :type api_secret: str
        """

        self.server = server
        self.api_key = api_key
        self.api_secret = api_secret
        self.verbose = verbose

    def get_person_id(self, person):
        v(self.verbose, 'getting person: {}'.format(person))
        headers = self._create_headers()
        params = {
            'person_handle': person
        }
        response = requests.get('{}/api/person'.format(self.server), headers=headers, params=params)
        if response.status_code == 200:
            matches = response.json()
            if len(matches) > 0:
                return matches[0]['_id']
        return None

    def _create_headers(self, more_headers={}):
        headers = dict()
        headers.update(more_headers)
        headers['X-API-KEY'] = self.api_key
        headers['X-API-SECRET-KEY'] = self.api_secret
        return headers

    def create_person(self, person):
        v(self.verbose, 'creating person: {}'.format(person))
        headers = self._create_headers({'Content-Type': 'application/json', 'Accept': 'application/json'})
        data = {
            'name': person,
            'person_handle': person,
            'gender': 0
        }
        response = requests.post('{}/api/person'.format(self.server), headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['_id']
        return None

    def add_lsm_content(self, person_id, content, recipient_id):
        v(self.verbose, 'add content for {}'.format(person_id))
        headers = self._create_headers({'Content-Type': 'application/json', 'Accept': 'application/json'})
        data = {
            'language_content': content,
            'recipient_id': recipient_id,
            'content_source': 6
        }
        response = requests.post('{}/api/person/{}/contents'.format(self.server, person_id), headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['_id']
        return None

    def get_lsm_score(self, id1, id2):
        v(self.verbose, 'get score for {} vs {}'.format(id1, id2))
        headers = self._create_headers({'Accept': 'application/json'})
        params = {
            'person1': id1,
            'person2': id2
        }
        response = requests.get('{}/api/lsm_score'.format(self.server), headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['lsm_score']
        return None

    def analyse(self, person1_name, person1_content, person2_name, person2_content):
        id1 = self.get_person_id(person1_name)
        if id1 is None:
            id1 = self.create_person(person1_name)

        id2 = self.get_person_id(person2_name)
        if id2 is None:
            id2 = self.create_person(person2_name)

        if self.add_lsm_content(id1, person1_content, id2) is None or self.add_lsm_content(id2, person2_content, id1) is None:
            print('Failed to add content')
        else:
            return self.get_lsm_score(id1, id2)


if __name__ == '__main__':
    import argparse
    import os

    class Person():
        def __init__(self, filename):
            # type: (filename) -> str
            self.name, self.content = self.extract(filename)

        def extract(self, filename):
            name = os.path.splitext(os.path.split(filename)[1])[0]
            with open(filename, mode='r') as f:
                text = f.read()
            return name, text


    description = '''Get the LSM score between 2 speakers. Pass in two files. Each file contains the text for one of the speakers and is named
    for that speaker. The text and names are used to create the speakers via the Receptiviti
    API, to add the text and to obtain the score.
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--server', type=str, help='server to use for analysis', default='https://app.receptiviti.com')
    parser.add_argument('--verbose', '-v', help='verbose output', action='store_true')
    parser.add_argument('key', type=str, help='API key')
    parser.add_argument('secret', type=str, help='API secret key')
    parser.add_argument('file1', type=str, help='file containing text for first speaker')
    parser.add_argument('file2', type=str, help='file containing text for second speaker')

    args = parser.parse_args()


    v(args.verbose, 'reading {}'.format(args.file1))
    person1 = Person(args.file1)
    v(args.verbose, 'reading {}'.format(args.file2))
    person2 = Person(args.file2)

    lsm = Receptiviti(args.server, args.key, args.secret, args.verbose)

    v(args.verbose, 'analysing...')
    print('score: {}'.format(lsm.analyse(person1.name, person1.content, person2.name, person2.content)))
