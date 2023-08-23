import json
import logging
import zlib

import pytest

import rasa_sdk.endpoint as ep
from rasa_sdk.events import SlotSet

# noinspection PyTypeChecker
app = ep.create_app(None)


logger = logging.getLogger(__name__)


def test_endpoint_exit_for_unknown_actions_package():
    with pytest.raises(SystemExit):
        ep.create_app("non-existing-actions-package")


def test_server_health_returns_200():
    request, response = app.test_client.get("/health")
    assert response.status == 200
    assert response.json == {"status": "ok"}


def test_server_list_actions_returns_200():
    request, response = app.test_client.get("/actions")
    assert response.status == 200
    assert len(response.json) == 5


def test_server_webhook_unknown_action_returns_404():
    data = {
        "next_action": "test_action_1",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    assert response.status == 404


def test_server_webhook_handles_action_exception():
    data = {
        "next_action": "custom_action_exception",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    assert response.status == 500
    assert response.json.get("error") == "test exception"
    assert response.json.get("request_body") == data


def test_server_webhook_custom_action_returns_200():
    data = {
        "next_action": "custom_action",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    events = response.json.get("events")

    assert events == [SlotSet("test", "bar")]
    assert response.status == 200


def test_server_webhook_custom_action_with_params_returns_200():
    data = {
        "next_action": "custom_action_with_params_dummy",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
        "domain": {
            "actions_params": {
                "custom_action_with_params_dummy": {
                    "base_action": "custom_action_with_params",
                    "args": ["test_args_1", "test_args_2"],
                    "kwargs": {"kwargs1": "test_kwargs1"},
                }
            }
        },
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    events = response.json.get("events")

    assert events == [
        SlotSet("args", "('test_args_1', 'test_args_2')"),
        SlotSet("kwargs", "{'kwargs1': 'test_kwargs1'}"),
    ]
    assert response.status == 200


def test_server_webhook_custom_action_with_wrong_params_returns_200():
    data = {
        "next_action": "custom_action_with_params_dummy",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
        "domain": {
            "actions_params": {
                "custom_action_with_params_dummy": {
                    "base_action": "custom_action_with_params",
                    "args": ["test_args_1", "test_args_2"],
                    "kwargs": {"domain": "test_kwargs1"},
                }
            }
        },
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    events = response.json.get("events")

    assert events == [
        SlotSet("args", "('test_args_1', 'test_args_2')"),
        SlotSet("kwargs", "{}"),
    ]
    assert response.status == 200


def test_server_webhook_custom_async_action_returns_200():
    data = {
        "next_action": "custom_async_action",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    events = response.json.get("events")

    assert events == [SlotSet("test", "foo"), SlotSet("test2", "boo")]
    assert response.status == 200


def test_server_webhook_custom_async_action_with_params_returns_200():
    data = {
        "next_action": "custom_async_action_with_params_dummy",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
        "domain": {
            "actions_params": {
                "custom_async_action_with_params_dummy": {
                    "base_action": "custom_async_action_with_params",
                    "args": ["test_args_1", "test_args_2"],
                    "kwargs": {"kwargs1": "test_kwargs1"},
                }
            }
        },
    }
    request, response = app.test_client.post("/webhook", data=json.dumps(data))
    events = response.json.get("events")

    assert events == [
        SlotSet("args", "('test_args_1', 'test_args_2')"),
        SlotSet("kwargs", "{'kwargs1': 'test_kwargs1'}"),
    ]
    assert response.status == 200


def test_arg_parser_actions_params_folder_style():
    parser = ep.create_argument_parser()
    args = ["--actions", "actions/act"]

    with pytest.raises(BaseException) as e:
        parser.parse_args(args)
    if e is not None:
        assert True
    else:
        assert False


def test_arg_parser_actions_params_module_style():
    parser = ep.create_argument_parser()
    args = ["--actions", "actions.act"]
    cmdline_args = parser.parse_args(args)
    assert cmdline_args.actions == "actions.act"


def test_server_webhook_custom_action_encoded_data_returns_200():
    data = {
        "next_action": "custom_action",
        "tracker": {"sender_id": "1", "conversation_id": "default"},
        "domain": {"intents": ["greet", "goodbye"]},
    }

    request, response = app.test_client.post(
        "/webhook",
        data=zlib.compress(json.dumps(data).encode()),
        headers={"Content-encoding": "deflate"},
    )
    events = response.json.get("events")

    assert events == [SlotSet("test", "bar")]
    assert response.status == 200
