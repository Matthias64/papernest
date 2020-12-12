import pytest
import requests_mock
from flask import json
from werkzeug.exceptions import HTTPException

from app.api.network_coverage import get_coordinates_from_address
from helpers.initialize_db_content import initialize_operators, initialize_positions
# noinspection PyUnresolvedReferences
from test.test_fixtures import app, client, db, session


def test_get_coordinates_from_address_ok():
    with requests_mock.Mocker() as mocker:
        with open("test/resources/json_output_example.json") as test_file:
            mocker.get(requests_mock.ANY, json=json.load(test_file))
            coordinates = get_coordinates_from_address("address_test")
            assert coordinates == [2.290084, 49.897443]


def test_get_coordinates_from_address_invalid():
    with requests_mock.Mocker() as mocker:
        with open("test/resources/json_output_example_invalid.json") as test_file:
            mocker.get(requests_mock.ANY, json=json.load(test_file))
            try:
                coordinates = get_coordinates_from_address("address_test")
                assert False
            except HTTPException as e:
                assert e.code == 500
                assert "was malformed and could not be read." in e.description


def test_get_coordinates_from_address_bad_request():
    with requests_mock.Mocker() as mocker:
        with open("test/resources/json_output_example_bad_request.json") as test_file:
            mocker.get(requests_mock.ANY, json=json.load(test_file))
            try:
                coordinates = get_coordinates_from_address("address_test")
                assert False
            except HTTPException as e:
                assert e.code == 400
                assert "Could not find any valid address for the input provided" in e.description


def test_get_coordinates(client, session):
    initialize_operators(session)
    initialize_positions(session, "test/resources/sample_mobile_sites.csv")
    with requests_mock.Mocker() as mocker:
        with open("test/resources/json_output_example.json") as test_file:
            mocker.get(requests_mock.ANY, json=json.load(test_file))
            response = client.get('/api/address_coordinates/address_test', follow_redirects=True)
            assert response.status_code == 200
            assert response.json == [2.290084, 49.897443]


@pytest.mark.parametrize('distance, expected', [
    [None, [{"Operator": "Orange", "2G": True, "3G": False, "4G": False}]],
    [1000.0, [{"Operator": "Orange", "2G": True, "3G": False, "4G": False}]],
    [100.0, []],
    [3000.0, [{"Operator": "Orange", "2G": True, "3G": False, "4G": False},
              {"Operator": "Free", "2G": True, "3G": False, "4G": False},
              {"Operator": "Bouygues", "2G": False, "3G": False, "4G": True}]],
    [600000.0, [{"Operator": "Orange", "2G": True, "3G": False, "4G": True},
                {"Operator": "Free", "2G": True, "3G": True, "4G": True},
                {"Operator": "Bouygues", "2G": False, "3G": True, "4G": True}]],
    [700000.0, [{"Operator": "Orange", "2G": True, "3G": False, "4G": True},
                {"Operator": "Free", "2G": True, "3G": True, "4G": True},
                {"Operator": "Bouygues", "2G": False, "3G": True, "4G": True},
                {"Operator": "SFR", "2G": True, "3G": True, "4G": True}]],
])
def test_get_coverage(client, session, distance, expected):
    initialize_operators(session)
    initialize_positions(session, "test/resources/sample_mobile_sites_pb.csv")
    with requests_mock.Mocker() as mocker:
        with open("test/resources/json_output_example_home.json") as test_file:
            mocker.get(requests_mock.ANY, json=json.load(test_file))
            address = '/api/network_coverage/address_test' + ("/" + str(distance) if distance else "")
            response = client.get(address, follow_redirects=True)
            assert response.status_code == 200
            assert sorted(sorted(d.items()) for d in response.json) == sorted(sorted(d.items()) for d in expected)
