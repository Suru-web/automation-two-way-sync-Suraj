import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SHEETS_CREDS = os.getenv("GOOGLE_SHEETS_CREDS_JSON")  # path to JSON
SHEET_NAME = os.getenv("SHEET_NAME", "LeadTracker")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


class LeadClient:
    def __init__(self):
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDS, scopes=SCOPES
        )
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(SHEET_NAME).sheet1

    def get_all_leads(self):
        data = self.sheet.get_all_records()
        return data

    def update_lead_status(self, lead_id, new_status):
        records = self.sheet.get_all_records()
        for i, row in enumerate(records, start=2):  # row 2 onwards
            if str(row["id"]) == str(lead_id):
                self.sheet.update_cell(i, 4, new_status)  # column 4 = status
                print(f"Updating Sheet → lead {lead_id} to status {new_status}")
                return True
        return False

    def store_trello_card_id(self, lead_id, card_id):
        records = self.sheet.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row["id"]) == str(lead_id):
                self.sheet.update_cell(i, 6, card_id)  # col 6 = trello_card_id
                return True
        return False
