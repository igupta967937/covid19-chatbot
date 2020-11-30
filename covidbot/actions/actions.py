# This files contains your custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
import requests
import smtplib
from utils.utils import create_covid_distribution_plot, create_covid_map_plot, upload_to_imgur

class ActionSendEmail(Action):
    def name(self) -> Text:
        return "action_send_email"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        recipient_email = tracker.get_slot('recipient_email')

        sender_email = "rev123iver@gmail.com"
        sender_pswd = "rev321iver"

        # connect to smtp server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_pswd)

        response = requests.get(
            "https://api.covid19india.org/data.json").json()

        for state_data in response["statewise"]:
            if state_data["state"] == "Total":
                # covid stats message
                message = state_data["state"] + \
                    "\nActive cases: " + state_data["active"] + \
                    "\nConfirmed cases: " + state_data["confirmed"] + \
                    "\nDeaths: " + state_data["deaths"] + \
                    "\nRecovered cases: " + state_data["recovered"] + \
                    "\nLast Updated: " + state_data["lastupdatedtime"]

        server.sendmail(  # send the email
            sender_email,
            recipient_email,
            message)
        server.quit()

        dispatcher.utter_message("Email sent!")

        return [SlotSet("recipient_email", None)]


# class ActionSendEmail(Action):

#     def name(self) -> Text:
#         return "action_send_email"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         recipient_email = tracker.get_slot('recipient_email')

#         sender_email = "rev123iver@gmail.com"
#         sender_pswd = "rev321iver"

#         # connect to smtp server
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server.login(sender_email, sender_pswd)

#         response = requests.get(
#             "https://api.covid19india.org/data.json").json()

#         for state_data in response["statewise"]:
#             if state_data["state"] == "Total":
#                 # covid stats message
#                 message = state_data["state"] + \
#                     "\nActive cases: " + state_data["active"] + \
#                     "\nConfirmed cases: " + state_data["confirmed"] + \
#                     "\nDeaths: " + state_data["deaths"] + \
#                     "\nRecovered cases: " + state_data["recovered"] + \
#                     "\nLast Updated: " + state_data["lastupdatedtime"]

#         server.sendmail(  # send the email
#             sender_email,
#             recipient_email,
#             message)
#         server.quit()

#         dispatcher.utter_message("Email sent!")
#         return []


class ActionShowCovidCasesDistribution(Action):

    def name(self) -> Text:
        return "action_show_covid_distribution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        local_img_path = create_covid_distribution_plot()
        img_url = upload_to_imgur(local_img_path)

        dispatcher.utter_message(image=img_url)

        return []


class ActionShowCovidCasesMap(Action):

    def name(self) -> Text:
        return "action_show_covid_map"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        local_img_path = create_covid_map_plot()
        img_url = upload_to_imgur(local_img_path)

        dispatcher.utter_message(image=img_url)

        return []


class ActionCovidTracker(Action):

    def name(self) -> Text:
        return "action_covid_state_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(
            "https://api.covid19india.org/data.json").json()

        entities = tracker.latest_message['entities']
        print("Last Message Now ", entities)
        state = None

        for e in entities:
            if e['entity'] == "state":
                state = e['value']

        # fallback message
        message = "I could not understand your input. Please enter a valid input statement."

        # change name to maintain compatibility with API
        if state == "india":
            state = "Total"

        for state_data in response["statewise"]:
            if state_data["state"] == state.title():
                # covid stats message
                message = state_data["state"] + \
                    "\nActive cases: " + state_data["active"] + \
                    "\nConfirmed cases: " + state_data["confirmed"] + \
                    "\nDeaths: " + state_data["deaths"] + \
                    "\nRecovered cases: " + state_data["recovered"] + \
                    "\nLast Updated: " + state_data["lastupdatedtime"]

        dispatcher.utter_message(text=message)

        return []
