#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
import argparse
import json

import requests
from os.path import isfile, join


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
        if response.status_code != 200:
            v(self.verbose, 'Http Response: {}'.format(response))
            raise Exception("Creating person failed!")

        return response.json()['_id']

    def add_content(self, person_id, content):
        v(self.verbose, 'add content for {}'.format(person_id))
        headers = self._create_headers({'Content-Type': 'application/json', 'Accept': 'application/json'})
        data = {
            'language_content': content,
            'content_source': 6
        }
        response = requests.post('{}/api/person/{}/contents'.format(self.server, person_id), headers=headers,
                                 data=json.dumps(data))

        if response.status_code != 200:
            raise Exception("Adding content failed!")

        return response.json()['_id']

    def get_profile(self, person_id):
        v(self.verbose, 'get profile for {}'.format(person_id))
        headers = self._create_headers({'Accept': 'application/json'})
        response = requests.get('{}/api/person/{}/profile'.format(self.server, person_id), headers=headers)
        if response.status_code != 200:
            raise Exception("Get profile failed!")
        return response.json()

    def get_communication_recommendation(self, person_name, person_contents):
        person_id = self.get_person_id(person_name)
        if person_id is None:
            person_id = self.create_person(person_name)
        for content in person_contents:
            self.add_content(person_id, content)
        return self.get_profile(person_id)["communication_recommendation"]


def get_person_contents():
    dir_path = os.path.join(os.path.dirname(__file__), 'content')
    content_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(".txt")]
    person_contents = []
    for content_file in content_files:
        with open(content_file, "r") as the_file:
            person_contents.append(the_file.readlines())

    return person_contents


if __name__ == '__main__':
    import os
    from os import listdir

    description = '''Get the Communication Recommendation for a Person.'''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--server', type=str, help='server to use for analysis', default='https://app.receptiviti.com')
    parser.add_argument('--verbose', '-v', help='verbose output', action='store_true')
    parser.add_argument('--key', type=str, help='API key')
    parser.add_argument('--secret', type=str, help='API secret key')
    parser.add_argument('--name', type=str, help='Person name', default="John Doe")

    args = parser.parse_args()

    receptiviti = Receptiviti(args.server, args.key, args.secret, args.verbose)

    v(args.verbose, 'analysing...')

    get_person_contents()

    print("Recommendations: {}".format(
        receptiviti.get_communication_recommendation(args.name, get_person_contents())))
