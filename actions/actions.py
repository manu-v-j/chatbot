# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
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

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionRecommendMusic(Action):
    def name(self) -> str:
        return "action_recommend_music"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        genre = tracker.get_slot("genre")
        
        # API key for Last.fm (replace with your actual API key)
        API_KEY = "457b45265e23f1b5d6afaa2453d8b019"

        # Validate genre
        if not genre:
            dispatcher.utter_message(text="Please provide a genre like rock, pop, or jazz.")
            return []

        # Last.fm API endpoint with updated search parameters
        url = f"https://ws.audioscrobbler.com/2.0/?method=track.search&track={genre}&api_key={API_KEY}&format=json"

        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Check if the data is available and has trackmatches
        if data and 'results' in data and 'trackmatches' in data['results']:
            tracks = data['results']['trackmatches']['track']
            
            if tracks:
                # Iterate through tracks and extract details for the first one
                track = tracks[0]
                song_title = track['name']
                artist = track['artist']
                url = track['url']
                listeners = track.get('listeners', 'N/A')
                
                # Get the largest available image URL if present
                image_url = next((img['#text'] for img in track['image'] if img['size'] == 'extralarge'), "No image available")

                dispatcher.utter_message(
                    text=(
                        f"How about listening to '{song_title}' by '{artist}'? "
                        
                    )
                )
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any tracks for the {genre} genre.")
        else:
            dispatcher.utter_message(text="Sorry, there was an issue fetching music recommendations.")
        
        return []
