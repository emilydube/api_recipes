#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
# Author: Abdul Gani
#
#
import pytest
from requests import *
import conftest


@pytest.mark.person_api
def test_profile_twitter_profile(baseurl, apikey, apisecret, twitter_handle):
    headers = conftest.auth_headers(apikey, apisecret)

    response = import_twitter_user(conftest.twitter_import_user_api_url(baseurl), headers, twitter_handle)
    expect(response.status_code).to(equal(200))

    status_check_url = "{}{}".format(baseurl, response.json()["_links"]["self"]["href"])
    latest_response = response.json()
    idx = 1
    while latest_response["status"] not in ["completed", "failed", "errored"]:
        time.sleep(5)
        response = get(status_check_url, headers=headers)
        expect(response.status_code).to(equal(200))
        latest_response = response.json()
        print("Retry {}: Status - {}. Last updated = {}".format(idx, latest_response["status"], latest_response["updated"]))
        idx += 1
    expect(latest_response["result"]["success"]).to(equal(5))
