from typing import List, Dict, Text, Any, Optional

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

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[Text, Any]] = None,
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


class CustomActionWithParams(ActionWithParams):
    def name(cls) -> Text:
        return "custom_action_with_params"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[Text, Any]] = None,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("args", str(args)), SlotSet("kwargs", str(kwargs))]
