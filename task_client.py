import os
import requests
from dotenv import load_dotenv

load_dotenv()

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

BASE_URL = "https://api.trello.com/1"


class TrelloClient:
    def __init__(self):
        self.auth = {
            "key": TRELLO_KEY,
            "token": TRELLO_TOKEN
        }

    def get_boards(self):
        url = f"{BASE_URL}/members/me/boards"
        r = requests.get(url, params=self.auth)
        r.raise_for_status()
        return r.json()

    def get_lists(self, board_id):
        url = f"{BASE_URL}/boards/{board_id}/lists"
        r = requests.get(url, params=self.auth)
        r.raise_for_status()
        return r.json()

    def create_card(self, list_id, name, desc=""):
        url = f"{BASE_URL}/cards"
        params = {
            **self.auth,
            "idList": list_id,
            "name": name,
            "desc": desc
        }
        r = requests.post(url, params=params)
        r.raise_for_status()
        return r.json()

    def move_card(self, card_id, list_id):
        url = f"{BASE_URL}/cards/{card_id}"
        params = {
            **self.auth,
            "idList": list_id
        }
        r = requests.put(url, params=params)
        r.raise_for_status()
        return r.json()

    def get_cards(self, list_id):
        url = f"{BASE_URL}/lists/{list_id}/cards"
        r = requests.get(url, params=self.auth)
        r.raise_for_status()
        return r.json()
