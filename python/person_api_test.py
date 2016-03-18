import json
from expects import expect, equal
from expects.matchers.built_in import be_none
from expects.matchers.built_in.have_keys import have_key
import pytest
from requests import *
import conftest
import factories


@pytest.mark.person_api
def test_create_person_with_writing_sample(baseurl, apikey, apisecret):

    writing_sample_data = factories.get_writing_sample_data()
    person_data = factories.get_person_data(writing_sample_data)

    person_api_url = conftest.person_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(person_api_url, json=person_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json["name"]).to(equal(person_data["name"]))
    expect(response_json["writing_samples"][0]).to(have_key("receptiviti_scores"))
    expect(response_json["writing_samples"][0]).to(have_key("liwc_scores"))

@pytest.mark.person_api
def test_create_person_only(baseurl, apikey, apisecret):
    person_data = factories.get_person_data()
    person_api_url = conftest.person_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(person_api_url, json=person_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json["name"]).to(equal(person_data["name"]))



