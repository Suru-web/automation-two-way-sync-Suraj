import logging
from lead_client import LeadClient
from task_client import TrelloClient
from mappings import LEAD_TO_TRELLO, TRELLO_TO_LEAD

class SyncService:
    def __init__(self):
        self.leads = LeadClient()
        self.trello = TrelloClient()

        # Cache list IDs by name
        self.list_ids = {}
    
    def load_list_ids(self, board_id):
        lists = self.trello.get_lists(board_id)
        self.list_ids = {l["name"]: l["id"] for l in lists}

    def initial_sync(self, board_id):
        """
        For each lead in sheet that doesn't have a Trello card yet → create one.
        """
        leads = self.leads.get_all_leads()

        for lead in leads:
            lead_id = lead["id"]
            status = lead["status"]
            name = lead["name"]
            email = lead["email"]
            trello_card_id = lead.get("trello_card_id", "")

            # Skip if already has Trello card
            if trello_card_id:
                continue

            trello_status = LEAD_TO_TRELLO.get(status, "TODO")
            list_id = self.list_ids[trello_status]

            desc = f"{name}\n{email}"

            # Create Trello card
            card = self.trello.create_card(list_id, name, desc)
            card_id = card["id"]

            # Store Trello card ID back to sheet
            self.leads.store_trello_card_id(lead_id, card_id)

            logging.info(f"Created Trello card for lead {lead_id}: {card_id}")

    def sync_leads_to_tasks(self, board_id):
        """
        If sheet status changes → move Trello card.
        """
        leads = self.leads.get_all_leads()

        for lead in leads:
            lead_id = lead["id"]
            status = lead["status"]
            trello_card_id = lead.get("trello_card_id", "")

            if not trello_card_id:
                continue

            trello_status = LEAD_TO_TRELLO.get(status)
            if not trello_status:
                continue

            target_list_id = self.list_ids[trello_status]

            # Move card
            self.trello.move_card(trello_card_id, target_list_id)
            logging.info(f"Moved Trello card {trello_card_id} → {trello_status}")

    def sync_tasks_to_leads(self, board_id):
        """
        If Trello list changes → update sheet status.
        """
        leads = self.leads.get_all_leads()
        # Build lookup table: trello_id → lead row
        lead_map = {str(l["trello_card_id"]): l for l in leads}

        for list_name, list_id in self.list_ids.items():
            if list_name not in TRELLO_TO_LEAD:
                continue

            cards = self.trello.get_cards(list_id)

            for card in cards:
                card_id = card["id"]
                new_status = TRELLO_TO_LEAD[list_name]
                
                
                print("Reverse sync:", card_id, "→", new_status)

                if card_id in lead_map:
                    lead_id = lead_map[card_id]["id"]
                    self.leads.update_lead_status(lead_id, new_status)
                    logging.info(f"Updated sheet status for lead {lead_id} → {new_status}")
