# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from SymptomsDiagnosis import SymptomsDiagnosis

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


diagnosis_object = SymptomsDiagnosis()
diagnosis_object.train()

symptoms_suggested_so_far = []


class ActionSymptomsTracker(Action):

    def name(self) -> Text:
        return "action_symptoms_tracker"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the latest message from user
        latest_message = tracker.latest_message.get('text')

        # get users symptoms
        symptoms = tracker.get_slot("symptom_list")

        # check for symptoms 
        if symptoms is None:
            symptoms = []
        
        # add current sypmtom to symptoms list or state already noted
        if latest_message not in symptoms:
            symptoms.append(latest_message)   
        else:
            dispatcher.utter_message("आपने पहले से ही इस " + latest_message + " लक्षण ों का उल्लेख किया है")         

        # update slot for future use
        SlotSet("symptom_list", symptoms)

        # get suggestion of next symptom 
        suggested_symptoms = diagnosis_object.symptoms_suggester(symptoms, symptoms_suggested_so_far)

        # list for suggested symptoms
        already_suggested = []


        # check wether symptoms are already suggested or not
        for symp in suggested_symptoms:
            if symp not in symptoms and symp not in symptoms_suggested_so_far:
                already_suggested.append(symp)
        
        # if no suggestion are made so far 
        if len(already_suggested) == 0:
            dispatcher.utter_template('utter_alternative')
            return [SlotSet("symptom_list", symptoms)]

        # Reason : we want to update user for highest confidence symptoms already_suggested

        symptoms_suggested_so_far.append(str(already_suggested[0]))

        # Create response buttons
        buttons = [{"title": "हाँ ", "payload": str(already_suggested[0])},{"title":"नहीं", "payload": ""}]

        # Send message
        dispatcher.utter_message("आपने कहा था कि आपको : " + latest_message)
        dispatcher.utter_button_message("क्या आपके "+ str(already_suggested[0]) + " भी है?", buttons)
        


        return [SlotSet("symptom_list", symptoms)]
        

    

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return "action_diagnosis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get users symptoms
        symptoms = tracker.get_slot("symptom_list")

        # Get diagnosis
        diag = diagnosis_object.predict(symptoms)

        print(diag)

        # Send message
        dispatcher.utter_message("हमारे मॉडल ने " + str(diag) + " रोग की भविष्यवाणी की है |" )

        return []