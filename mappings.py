# Lead → Trello list mapping
LEAD_TO_TRELLO = {
    "NEW": "TODO",
    "CONTACTED": "IN_PROGRESS",
    "QUALIFIED": "IN_PROGRESS",
    "LOST": "DONE",
    "COMPLETED": "DONE"
}

# Trello → Lead mapping (reverse sync)
TRELLO_TO_LEAD = {
    "TODO": "NEW",
    "IN_PROGRESS": "CONTACTED",
    "DONE": "QUALIFIED",   # simple assumption
    "DONE": "COMPLETED"
}
