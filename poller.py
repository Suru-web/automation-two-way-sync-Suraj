import hashlib
import time
from sync_logic import SyncService

BOARD_ID = "69341c47343b00d03af0ffe1"

sync = SyncService()
sync.load_list_ids(BOARD_ID)


def sheet_hash():
    leads = sync.leads.get_all_leads()
    data = "".join([f"{l['id']}-{l['status']}" for l in leads])
    return hashlib.md5(data.encode()).hexdigest()


if __name__ == "__main__":
    last = None

    while True:
        current = sheet_hash()

        if last and current != last:
            print("Sheet changed → Syncing Sheet → Trello")
            sync.sync_leads_to_tasks(BOARD_ID)

        last = current
        time.sleep(10)
