from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.models.booking import Booking
from backend.models.driver_status import DriverStatus
from backend.services.booking_status_evaluator import BookingStatusEvaluator


@dataclass(frozen=True)
class CancellationPolicyResult:
    """ผลลัพธ์ตาม R1-R4 สำหรับนำไปอัปเดตสถานะคำขอยกเลิก"""

    decision: str
    booking_status: str
    refund_rate: float
    reason: str


class CancellationPolicy:
    """คำนวณ policy การยกเลิกตาม REQ-CMP-001, R2, R3, R4, AS-01, AS-04"""

    FULL_REFUND = "CANCELLED_FULL_REFUND"
    DEPOSIT_FORFEITED = "CANCELLED_DEPOSIT_FORFEITED"
    REJECTED = "CANCELLATION_REJECTED"
    ADMIN_REVIEW = "CANCELLATION_ADMIN_REVIEW"

    def __init__(self, evaluator: Optional[BookingStatusEvaluator] = None) -> None:
        self._evaluator = evaluator or BookingStatusEvaluator()

    # รองรับ: REQ-CMP-001, R2, R3, R4, AS-01, AS-04
    def evaluate(
        self,
        booking: Booking,
        driver_status: Optional[DriverStatus] = None,
        *,
        status_allows_cancellation: bool,
        now: Optional[datetime] = None,
        threshold_minutes: int = 120,
    ) -> CancellationPolicyResult:
        evaluation = self._evaluator.evaluate(
            booking,
            driver_status,
            status_allows_cancellation=status_allows_cancellation,
            now=now,
        )

        if not evaluation.status_allows_cancellation or evaluation.driver_departed:
            return CancellationPolicyResult(
                decision=self.REJECTED,
                booking_status="CANCELLATION_REJECTED",
                refund_rate=0.0,
                reason="สถานะการจองไม่อนุญาตให้ยกเลิกหรือคนขับออกเดินทางแล้ว",
            )

        if not evaluation.driver_confirmed:
            return CancellationPolicyResult(
                decision=self.FULL_REFUND,
                booking_status=self.FULL_REFUND,
                refund_rate=100.0,
                reason="ยังไม่มีคนขับรับงาน",
            )

        if evaluation.remaining_minutes <= threshold_minutes:
            return CancellationPolicyResult(
                decision=self.DEPOSIT_FORFEITED,
                booking_status=self.DEPOSIT_FORFEITED,
                refund_rate=0.0,
                reason="คนขับรับงานแล้วและเหลือเวลาไม่เกิน 120 นาที",
            )

        return CancellationPolicyResult(
            decision=self.ADMIN_REVIEW,
            booking_status="PENDING_ADMIN_REVIEW",
            refund_rate=0.0,
            reason="คนขับรับงานแล้วและเหลือเวลามากกว่า 120 นาที",
        )