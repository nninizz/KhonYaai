from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.models.booking import Booking
from backend.models.driver_status import DriverStatus


@dataclass(frozen=True)
class BookingStatusEvaluation:
    """ข้อเท็จจริงที่ policy engine ใช้ตัดสินการยกเลิก"""

    remaining_minutes: int
    driver_confirmed: bool
    driver_departed: bool
    status_allows_cancellation: bool


class BookingStatusEvaluator:
    """ประเมินเวลาและสถานะการจองสำหรับ REQ-CMP-001, R2, R3, R4, AS-01, AS-04"""

    # รองรับ: REQ-CMP-001, R2, R3, R4, AS-01, AS-04
    def evaluate(
        self,
        booking: Booking,
        driver_status: Optional[DriverStatus] = None,
        *,
        status_allows_cancellation: bool,
        now: Optional[datetime] = None,
    ) -> BookingStatusEvaluation:
        current_driver_status = driver_status or DriverStatus(driver_id=booking.driver_id or "")
        return BookingStatusEvaluation(
            remaining_minutes=booking.remaining_minutes(now),
            driver_confirmed=booking.is_driver_confirmed(),
            driver_departed=current_driver_status.is_departed(),
            status_allows_cancellation=status_allows_cancellation,
        )