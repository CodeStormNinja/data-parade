from datetime import datetime, timezone

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def utc_to_timestamp(utc_str: str) -> float:
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return dt.timestamp()