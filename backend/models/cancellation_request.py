from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

# รองรับ: REQ-CMP-001, UC-01, AS-01, AS-03
@dataclass
class CancellationRequest:
    request_id: str
    booking_id: str
    customer_id: str
    reason: Optional[str] = None
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    action_by: str = 'customer'
    result_status: str = 'pending'
    refund_rate: float = 0.0

    def is_refund_full(self) -> bool:
        return self.result_status in {'cancelled_full_refund', 'refunded_full'} and self.refund_rate >= 100.0

    def is_deposit_forfeited(self) -> bool:
        return self.result_status in {'cancelled_deposit_forfeited', 'deposit_forfeited'}
