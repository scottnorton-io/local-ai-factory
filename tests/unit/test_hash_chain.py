import json
from hashlib import sha256
from pathlib import Path


def compute_record_hash(envelope: dict) -> str:
    payload_bytes = json.dumps(
        {
            "event": envelope["event"],
            "prev_hash": envelope["prev_hash"],
            "timestamp": envelope["timestamp"],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload_bytes).hexdigest()


def test_hash_chain_is_contiguous(tmp_path: Path) -> None:
    # Simulate three records appended to a log
    path = tmp_path / "evidence-test.jsonl"

    prev_hash = None
    records = []
    for i in range(3):
        env = {
            "timestamp": f"2025-12-24T00:00:0{i}Z",
            "prev_hash": prev_hash,
            "event": {"event_type": "test", "sequence": i},
        }
        record_hash = compute_record_hash(env)
        env["record_hash"] = record_hash
        prev_hash = record_hash
        records.append(env)

    with path.open("w", encoding="utf-8") as f:
        for env in records:
            f.write(json.dumps(env, separators=(",", ":")))
            f.write("\n")

    # Verify chain from file
    last_hash = None
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            assert rec["prev_hash"] == last_hash
            expected = compute_record_hash(rec)
            assert rec["record_hash"] == expected
            last_hash = rec["record_hash"]
          
