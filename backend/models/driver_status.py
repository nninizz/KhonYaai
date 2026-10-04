from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

# รองรับ: REQ-CMP-001, AS-04, R4
@dataclass
class DriverStatus:
    driver_id: str
    trip_status: str = 'idle'
    departed_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_departed(self) -> bool:
        return self.trip_status == 'departed' or (self.departed_at is not None)
