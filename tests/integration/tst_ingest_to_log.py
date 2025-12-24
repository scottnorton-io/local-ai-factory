import json
from pathlib import Path
from subprocess import run


def test_ingestion_writes_ingestion_events(tmp_path: Path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    data_dir = tmp_path / "data"
    inbox = data_dir / "inbox"
    logs = data_dir / "logs"
    inbox.mkdir(parents=True)
    logs.mkdir(parents=True)

    sample = inbox / "sample.md"
    sample.write_text("# Sample\n\nHello Local AI Factory!\n", encoding="utf-8")

    env = {
        "FACTORY_INBOX_DIR": str(inbox),
        "EVIDENCE_LOG_DIR": str(logs),
    }

    # Run ingestion main once
    run([
        "python",
        "-m",
        "services.ingestion.main",
    ], cwd=repo_root, check=True, env={**env, **dict(**env)})

    log_files = list(logs.glob("evidence-*.jsonl"))
    assert log_files, "Expected at least one evidence log file"

    found_ingestion = False
    for lf in log_files:
        with lf.open("r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                if record.get("event", {}).get("event_type") == "ingestion":
                    found_ingestion = True
                    break
    assert found_ingestion, "Expected at least one ingestion event in logs"
  
