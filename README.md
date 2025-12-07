# Two-Way Sync: Google Sheets ⇄ Trello

Software Engineer Intern — Automation & Integrations

## Overview

This project implements a **realistic two-way data synchronization** between:

* **Google Sheets** (Lead Tracker)
* **Trello** (Work Tracker)

The integration keeps **lead status** and **task status** in sync automatically using Python, REST APIs, and event-based automation.

### Key Features

✔ Two-way sync (Sheet → Trello and Trello → Sheet)
✔ Real Trello webhook (push-based reverse sync)
✔ Lightweight polling (pull-based forward sync)
✔ Idempotency — no duplicate Trello cards
✔ Logging for visibility and debugging
✔ Real REST API usage (requests, Trello API, Google Sheets API)

---

## Architecture

### Data Model

**Lead (Sheet)**

* id
* name
* email
* status
* source
* trello_card_id *(stored to maintain idempotency)*

**Task (Trello)**

* Trello card
* list name maps to lead status
* card id stored in sheet

### Sync Flow

* **Forward sync (Sheet → Trello):**
  A polling daemon monitors sheet changes using hashing. If a change is detected, Trello cards are created or moved accordingly.

* **Reverse sync (Trello → Sheet):**
  A Flask server receives Trello webhook events whenever a card is moved to a new list. The lead status in Google Sheets is updated automatically.

### Push / Pull Hybrid Architecture

* Google Sheets **has no outbound webhook**
  → solved via polling every 10 seconds

* Trello **supports outbound webhooks**
  → solved via `/webhook/trello` Flask endpoint

This design intentionally mirrors real integration tools (Zapier, n8n, Make).

---

## Project Structure

```
DEEPLOGIC ASSIGNMENT/
├── client/
│   ├── lead_client.py          # Sheets API wrapper
│   ├── task_client.py          # Trello API wrapper
│   ├── sync_logic.py           # Core synchronization logic
│   ├── mappings.py             # Status conversion tables
│
├── poller.py                   # Forward sync (Sheet → Trello)
├── server.py                   # Reverse sync (Trello → Sheet, webhook)
│
├── requirements.txt
├── service_account.json        # Google service account (ignored in .gitignore)
├── .env                        # Environment configuration (ignored in git)
└── README.md
```

---

## How to Setup

### 1. Clone the repository

```bash
git clone https://github.com/<username>/two-way-sync
cd two-way-sync
```

---

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Google Sheets Setup

1. Create a service account at:
   [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

2. Download the JSON credentials as `service_account.json`

3. In Google Sheets, create a sheet with columns:

```
id | name | email | status | source | trello_card_id
```

4. Share the sheet with your **service account email**
   (example: `my-service-account@project-id.iam.gserviceaccount.com`)

---

### 4. Trello API Setup

1. Get keys:
   [https://trello.com/app-key](https://trello.com/app-key)

2. Copy:

   * `TRELLO_KEY`
   * `TRELLO_TOKEN`

3. Create a Trello board with lists:

```
TODO
IN_PROGRESS
DONE
```

---

### 5. Environment Variables

Create `.env`

```
GOOGLE_SHEETS_CREDS_JSON=service_account.json
SHEET_NAME=LeadTracker

TRELLO_KEY=xxxx
TRELLO_TOKEN=xxxx
```

---

### 6. Start the Server (Reverse Sync)

```bash
python3 -m server
```

If you need webhook support:

```bash
ngrok http 5000
```

Register webhook:

```bash
curl -X POST \
"https://api.trello.com/1/webhooks/?key=$TRELLO_KEY&token=$TRELLO_TOKEN" \
-d "callbackURL=https://<YOUR_NGROK>.ngrok-free.app/webhook/trello" \
-d "idModel=<YOUR_BOARD_ID>"
```

---

### 7. Start the Poller (Forward Sync)

```bash
python3 -m poller
```

The system is now **fully automatic**.

* Edit Google Sheets → Trello updates in <10 seconds
* Move cards in Trello → Sheets updates instantly

---

## Status Mappings

Mappings are defined in `mappings.py`

```python
LEAD_TO_TRELLO = {
    "NEW": "TODO",
    "CONTACTED": "IN_PROGRESS",
    "QUALIFIED": "IN_PROGRESS",
    "COMPLETED": "DONE",
    "LOST": "DONE"
}

TRELLO_TO_LEAD = {
    "TODO": "NEW",
    "IN_PROGRESS": "CONTACTED",
    "DONE": "COMPLETED",
    "DONE": "COMPLETED"
}
```

---

##
