# -*- coding: utf-8 -*-

import pytest

content = '''
It’s systematic in that you don’t just metaphorically describe anything as anything else.
Instead, it’s mostly abstract things that you describe in terms of concrete things.
Morality is more abstract than cleanliness. Understanding is more abstract than seeing.
And you can’t reverse the metaphors. While you can say “He’s clean” to mean he has no
criminal record, you can’t say “He’s moral” to mean that he bathed recently.
Metaphor is unidirectional, from concrete to abstract.

Metaphorical expressions are also coherent with one another. Take the example of
understanding and seeing. There are lots of relevant metaphorical expressions, for
example “I see what you mean,” and “Let’s shed some light on the issue,” and “Put
his idea under a microscope and see if it actually makes sense.” And so on. While
these are totally different metaphorical expressions—they use completely different
words—they all coherently cast certain aspects of understanding in terms of specific
aspects of seeing. You always describe the understander as the seer, the understood
idea as the seen object, the act of understanding as seeing, the understandability
of the idea as the visibility of the object, and so on. In other words, the aspects
of seeing you use to talk about aspects of understanding stand in a fixed mapping
to one another.
'''


def pytest_addoption(parser):
    parser.addoption("--baseurl", action="store", default="https://app.receptiviti.com", help="Specify this in the format https://<target_domain_name>")
    parser.addoption("--key", action="store", default=None, help="The API key for the test user")
    parser.addoption("--secret", action="store", default=None, help="The API secret for the test user")


@pytest.fixture
def baseurl(request):
    return request.config.getoption("--baseurl")


@pytest.fixture
def apikey(request):
    return request.config.getoption("--key")


@pytest.fixture
def apisecret(request):
    return request.config.getoption("--secret")


@pytest.fixture
def twitter_handle():
    return 'anncoulter'


def twitter_import_user_api_url(baseurl):
    return "{}/import/twitter/user".format(api_base_url(baseurl))


def api_base_url(baseurl):
    return "{}/v2/api".format(baseurl)


def person_api_url(baseurl):
    return "{}/person".format(api_base_url(baseurl))

def merge_personality_api_url(baseurl):
    return "{}/person/merged_personality".format(api_base_url(baseurl))


def person_content_api_url(baseurl, person_id):
    return "{}/person/{}/contents".format(api_base_url(baseurl), person_id)


def upload_api_url(baseurl):
    return "{}/upload/upload_request".format(api_base_url(baseurl))


def ping_url(baseurl):
    return "{}/ping".format(api_base_url(baseurl))


def base_headers(apikey, apisecret):
    header = auth_headers(apikey, apisecret)
    header['Content-type'] = 'application/json'
    return header


def auth_headers(apikey, apisecret):
    header = {}
    if apikey:
        header['X-API-KEY'] = apikey
    if apisecret:
        header['X-API-SECRET-KEY'] = apisecret
    return header
