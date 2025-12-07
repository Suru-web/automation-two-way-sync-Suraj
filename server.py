from flask import Flask, request, jsonify
from sync_logic import SyncService

BOARD_ID = "69341c47343b00d03af0ffe1"

app = Flask(__name__)

sync = SyncService()
sync.load_list_ids(BOARD_ID)


@app.route("/", methods=["GET"])
def home():
    return "Trello Sync Server Running", 200


# ================================
# TRELO WEBOOK ENDPOINT
# ================================
@app.route("/webhook/trello", methods=["HEAD"])
def webhook_verify():
    # Trello performs a HEAD request to verify webhook
    return "", 200


@app.route("/webhook/trello", methods=["POST"])
def trello_webhook():
    data = request.json

    # DEBUG PRINT — see events come in
    print("Trello webhook event:", data)

    # RUN REVERSE SYNC (Trello → Sheet)
    sync.sync_tasks_to_leads(BOARD_ID)

    return jsonify({"status": "ok"}), 200


# ================================
# MANUAL SYNC ENDPOINTS (OPTIONAL)
# ================================
@app.route("/sync/sheet", methods=["GET"])
def sync_sheet_to_trello():
    sync.sync_leads_to_tasks(BOARD_ID)
    return jsonify({"message": "Sheet → Trello"})


@app.route("/sync/trello", methods=["GET"])
def sync_trello_to_sheet():
    sync.sync_tasks_to_leads(BOARD_ID)
    return jsonify({"message": "Trello → Sheet"})


if __name__ == "__main__":
    # IMPORTANT: must be on a public URL for Trello webhooks
    app.run(port=8080, debug=True)
