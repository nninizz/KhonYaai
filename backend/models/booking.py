from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

# รองรับ: REQ-CMP-001, UC-01, AS-01, AS-04
@dataclass
class Booking:
    booking_id: str
    customer_id: str
    driver_id: Optional[str]
    appointment_time: datetime
    current_status: str
    deposit_amount: float
    cancellation_policy: str = 'standard'
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def remaining_minutes(self, now: Optional[datetime] = None) -> int:
        reference_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        remaining_seconds = (self.appointment_time.astimezone(timezone.utc) - reference_time).total_seconds()
        return max(0, int(remaining_seconds // 60))

    def is_within_cancellation_window(self, threshold_minutes: int = 120, now: Optional[datetime] = None) -> bool:
        return self.remaining_minutes(now) <= threshold_minutes

    def is_driver_confirmed(self) -> bool:
        return self.driver_id is not None and self.current_status in {'driver_confirmed', 'accepted', 'assigned'}
