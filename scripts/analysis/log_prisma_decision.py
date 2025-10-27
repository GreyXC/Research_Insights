import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("data_sources_raw/logs/prisma_decisions.jsonl")

def log_decision(record_id, stage, decision, reason):
    entry = {
        "id": record_id,
        "stage": stage,
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat()
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")