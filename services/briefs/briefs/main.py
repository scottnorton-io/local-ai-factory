from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from services.common.events import DailyBriefEvent, DailyBriefPayload, make_event


def generate_brief(now: datetime | None = None) -> DailyBriefEvent:
    now = now or datetime.utcnow()
    start = now - timedelta(days=1)
    brief_dir = Path("data/briefs")
    brief_dir.mkdir(parents=True, exist_ok=True)

    brief_path = brief_dir / f"{now.date()}_daily_brief.md"
    brief_path.write_text("# Daily Brief\n\n(Stub contents)", encoding="utf-8")

    payload = DailyBriefPayload(
        brief_path=str(brief_path),
        num_items=0,
        period_start=start,
        period_end=now,
    )
    return DailyBriefEvent(event_type="daily_brief", service="briefs", payload=payload)


if __name__ == "__main__":
    ev = generate_brief()
    print(ev)
  
