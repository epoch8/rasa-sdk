from typing import List, Dict, Text, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import ActionWithParams
from rasa_sdk.types import DomainDict


class CustomAsyncAction(Action):
    def name(cls) -> Text:
        return "custom_async_action"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("test", "foo"), SlotSet("test2", "boo")]


class CustomAsyncActionWithParams(ActionWithParams):
    def name(cls) -> Text:
        return "custom_async_action_with_params"

    @staticmethod
    def description():
        return {
            "description": "CustomAsyncActionWithParams description",
            "args": [
                {"description": "test_arg1", "type": "str"},
                {"description": "test_arg2", "type": "str"},
            ],
            "kwargs": [
                {
                    "name": "test_kwarg1",
                    "description": "kwarg1_description",
                    "type": "int",
                },
                {
                    "name": "test_kwarg2",
                    "description": "kwarg2_description",
                    "type": "bool",
                },
            ],
        }

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        *args,
        **kwargs,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("args", str(args)), SlotSet("kwargs", str(kwargs))]


class CustomAction(Action):
    def name(cls) -> Text:
        return "custom_action"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("test", "bar")]


class CustomActionWithDesc(Action):
    def name(cls) -> Text:
        return "custom_action_with_description"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("test", "bar")]

    @staticmethod
    def description():
        return {"description": "test action description"}


class CustomActionWithParams(ActionWithParams):
    def name(cls) -> Text:
        return "custom_action_with_params"

    @staticmethod
    def description():
        return {
            "description": "CustomActionWithParams description",
            "kwargs": [
                {
                    "name": "test_kwarg1",
                    "description": "kwarg1_description",
                    "type": "int",
                },
            ],
        }

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        *args,
        **kwargs,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("args", str(args)), SlotSet("kwargs", str(kwargs))]
