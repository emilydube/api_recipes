import json
import random
from expects import expect, equal
from expects.matchers.built_in import be_above
from expects.matchers.built_in.have_keys import have_key
import pytest
from requests import *
import conftest
import factories


@pytest.mark.person_api
def test_create_person_with_content(baseurl, apikey, apisecret):

    content_data = factories.get_content_data()
    person_data = factories.get_person_data(content_data)

    person_api_url = conftest.person_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(person_api_url, json=person_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json["name"]).to(equal(person_data["name"]))
    expect(response_json["contents"][0]).to(have_key("receptiviti_scores"))
    expect(response_json["contents"][0]).to(have_key("liwc_scores"))


@pytest.mark.person_api
def test_create_person_only(baseurl, apikey, apisecret):
    person_data = factories.get_person_data()
    person_api_url = conftest.person_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(person_api_url, json=person_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json["name"]).to(equal(person_data["name"]))


@pytest.mark.person_api
def test_get_people_in_the_system(baseurl, apikey, apisecret):
    auth_headers = conftest.auth_headers(apikey, apisecret)

    people = get_all_people_in_the_system(auth_headers, baseurl)
    expect(len(people)).to(be_above(0))
    expect(people[0]).to(have_key("_id"))


@pytest.mark.person_api
def test_submit_sample_for_an_existing_person(baseurl, apikey, apisecret):
    auth_headers = conftest.auth_headers(apikey, apisecret)

    person = get_one_person(auth_headers, baseurl)
    sample_data = factories.get_content_data()

    create_sample_url = conftest.person_content_api_url(baseurl, person["_id"])
    print("*"*20)
    print("create_sample_url={}".format(create_sample_url))
    print("*"*20)

    response = post(create_sample_url, json=sample_data, headers=auth_headers)
    expect(response.status_code).to(equal(200))
    response_json = json.loads(response.content)

    expect(response_json).to(have_key("receptiviti_scores"))
    expect(response_json).to(have_key("liwc_scores"))
    expect(response_json["content_handle"]).to(equal(sample_data["content_handle"]))


def get_one_person(auth_headers, baseurl):
    people = get_all_people_in_the_system(auth_headers, baseurl)
    return people[random.randint(0, len(people))]


def get_all_people_in_the_system(auth_headers, baseurl):
    person_api_url = conftest.person_api_url(baseurl)
    response = get(person_api_url, headers=auth_headers)
    expect(response.status_code).to(equal(200))
    people = json.loads(response.content)
    return people
