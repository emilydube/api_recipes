import json

from expects import expect, equal
from expects.matchers.built_in.have_keys import have_key
from expects.matchers.built_in.start_end_with import start_with
from requests import *

from . import conftest
from . import factories


def test_ping(baseurl, apikey, apisecret):
    ping_url = conftest.ping_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)
    print "PING URL:---------> " + ping_url

    response = get(ping_url, headers=auth_headers)

    response_json = json.loads(response.content)
    print response_json
    expect(response.status_code).to(equal(200))
    expect(response_json["pong"]).to(start_with("Hello"))


def test_score_content(baseurl, apikey, apisecret):
    content_data = factories.get_content_data()

    content_api_url = conftest.content_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(content_api_url, json=content_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json).to(have_key("receptiviti_scores"))
    expect(response_json).to(have_key("liwc_scores"))
    _print_interesting_content_information(response_json)


def _print_interesting_content_information(response_json):
    print(("Authenticity Score: {}".format(response_json["liwc_scores"]["authentic"])))
    print(("Thinking Style: {}".format(response_json["receptiviti_scores"]["percentiles"]["thinking_style"])))
    print(("Personality Snapshot: {}".format(response_json["personality_snapshot"])))
    print(("Communication Recommendation: {}".format(response_json["communication_recommendation"])))
