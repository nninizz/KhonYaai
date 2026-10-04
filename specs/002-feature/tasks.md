# Tasks | SPEC-CANCLE | การยกเลิกการจองบริการ

- Feature: การยกเลิกการจองบริการ
- Spec ID: SPEC-CANCLE
- อ้างอิง plan.md: plan.md
- วันที่: 2569-10-04
- Stack ที่ใช้: Frontend React + Vite + Tailwind; Backend FastAPI; Database PostgreSQL (ทีมเลือกเอง ไม่ได้มาจาก spec)
- สรุป: 7 task ทั้งหมด, ไม่มี task ที่ต้องรอ Open Questions จากทีม; งานที่ยังมี dependency ให้ยึดช่อง “ต้องทำหลัง”

## รายการ task

### T-01 ตั้งโครงโปรเจกต์และ test bootstrap
- รองรับ: REQ-CMP-001, UC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: frontend/src/, frontend/package.json, frontend/vite.config.js, frontend/tailwind.config.js, backend/app/, backend/requirements.txt, db/init.sql, docker-compose.yml
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: รัน frontend build หรือ backend smoke test เริ่มต้นผ่าน 1 ตัว โดยใช้ React + Vite + Tailwind และ FastAPI + PostgreSQL
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง model หลักของการจองและคำขอยกเลิก
- รองรับ: REQ-CMP-001, UC-01, AS-01, AS-04
- ตรวจด้วย: AC ใน §6 (ไม่มี ID ใน spec) สำหรับกรณีที่มีการยกเลิกก่อนรับงาน/หลังรับงาน/ก่อนถึง 120 นาที
- ไฟล์ที่แตะ: backend/models/booking.py, backend/models/cancellation_request.py, backend/models/driver_status.py, db/init.sql
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: model มี field ที่จำเป็นและสามารถคำนวณ remainingMinutes และ driverStatus ได้ โดยใช้ PostgreSQL schema ที่สอดคล้องกับ flow ยกเลิก
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้าง engine นโยบายยกเลิกและ boundary time
- รองรับ: REQ-CMP-001, R2, R3, R4, AS-01, AS-04
- ตรวจด้วย: AC ใน §6 สำหรับกรณี 120 นาที, มากกว่า 120 นาที และเริ่มงานแล้ว
- ไฟล์ที่แตะ: backend/services/cancellation_policy.py, backend/services/booking_status_evaluator.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ระบบสามารถคำนวณผลลัพธ์ได้ว่า คืนเต็ม / ริบมัดจำ / ปฏิเสธ / ส่งให้แอดมินตรวจสอบ ตามเงื่อนไขที่ระบุโดยใช้ boundary <= 120 นาที ตาม AS-01
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 สร้าง API ตรวจสิทธิ์และยกเลิกคำขอ
- รองรับ: UC-01, REQ-CMP-001, AS-02, AS-05
- ตรวจด้วย: AC ใน §6 สำหรับกรณียกเลิกและการปฏิเสธเมื่อเจ้าของบัญชีไม่ตรง
- ไฟล์ที่แตะ: backend/app/api/cancel_requests.py, backend/app/api/booking_policy.py, backend/app/api/admin_cancel_requests.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: POST /bookings/{bookingId}/cancel-requests และ GET /bookings/{bookingId}/cancel-policy ทำงานได้ตามสัญญา API และปฏิเสธ case ที่ไม่ใช่เจ้าของบัญชีใน FastAPI service
- สถานะ: พร้อมทำ

### T-05 สร้าง workflow แอดมินยกเลิกแทนและประมวลผลต่อ
- รองรับ: UC-01, AS-02, AS-05, §2, §5
- ตรวจด้วย: AC ใน §6 สำหรับกรณีที่ต้องส่งให้แอดมินตรวจสอบและกรณีบัญชีอื่นยกเลิกไม่ได้
- ไฟล์ที่แตะ: backend/app/admin/cancel_requests.py, backend/app/workflows/admin_override.py, frontend/src/pages/AdminCancelRequests.tsx
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: แอดมินสามารถเห็นคำขอ, ยืนยันเจ้าของบัญชี, และอนุมัติ/ปฏิเสธคำขอได้ตามห้วงเวลาและกฎผ่าน UI React และ API FastAPI
- สถานะ: พร้อมทำ

### T-06 สร้าง payment refund flow และ notification SMS
- รองรับ: REQ-CMP-001, §2, AS-01, AS-03, AS-06
- ตรวจด้วย: AC ใน §6 สองกรณีหลักคือ คืนเงินเต็ม/ริบมัดจำ และ SMS แจ้งผลภายใน 10 นาที
- ไฟล์ที่แตะ: backend/services/payment_refund.py, backend/services/notification_sms.py, backend/app/workflows/refund_processor.py, frontend/src/components/CancelResultCard.tsx
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: การคืนเงิน/ไม่คืนเงินและการส่ง SMS ให้ลูกค้าและคนขับเกิดขึ้นตามหลักเกณฑ์ และ refund สถานะพร้อมส่งต่อให้แอดมินติดตามเมื่อไม่สำเร็จผ่าน FastAPI + PostgreSQL
- สถานะ: พร้อมทำ

### T-07 สร้าง test ครอบคลุมทุก acceptance scenario และ contract validation
- รองรับ: REQ-CMP-001, UC-01, AS-01 ถึง AS-06
- ตรวจด้วย: AC ใน §6 ทั้งหมด
- ไฟล์ที่แตะ: frontend/src/__tests__/cancel-flow.test.tsx, backend/tests/test_cancel_flow.py, backend/tests/test_payment_refund.py, backend/tests/test_admin_override.py
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: test_AC_CANCEL_01 ถึง test_AC_CANCEL_07 ผ่านตามลำดับ และมีอธิบายความครอบคลุมของแต่ละ scenario ทั้ง frontend และ backend
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

### 1) ตาราง AC ID | task ที่ตรวจ AC นี้
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC ใน §6 (ไม่มี ID ใน spec) | T-02, T-03, T-04, T-05, T-06, T-07 |
| AC-ยกเลิกก่อนคนขับรับงาน | T-02, T-03, T-04, T-07 |
| AC-ยกเลิกหลังคนขับรับงานและเหลือเวลา <= 120 นาที | T-03, T-04, T-06, T-07 |
| AC-ยกเลิกมากกว่า 120 นาที | T-03, T-05, T-07 |
| AC-คนขับออกเดินทางแล้ว | T-03, T-04, T-07 |
| AC-บัญชีอื่นยกเลิกไม่ได้ | T-04, T-05, T-07 |
| AC-SMS ภายใน 10 นาที | T-06, T-07 |
| AC-คืนเงินไม่สำเร็จแจ้งแอดมิน | T-06, T-07 |

### 2) ตาราง Constraint ID | task ที่ทำให้เป็นจริง
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PDPA / การเก็บข้อมูล Thai-ID และที่อยู่บ้าน | T-01, T-02, T-04, T-05 |
| ต้องเก็บหลักฐานการยืนยันตัวตนตามระยะเวลาที่กฎหมายกำหนด | T-05 |
| ต้องไม่เก็บสำเนาบัตรประชาชนเมื่อตรวจผ่าน Thai-ID แล้ว | T-02, T-05 |
| AS-01 ถึง AS-06 | T-03, T-04, T-05, T-06, T-07 |

## สิ่งที่ยังไม่ทำ
- ไม่มี Q-xx ที่ระบุชัดเจนใน spec ณ ปัจจุบัน
- ข้อสรุปจากการ clarify ถูกบันทึกใน spec.md เป็น AS-01 ถึง AS-06 และ ASM-01 ถึง ASM-08
- T-05 และ T-06 ยังต้องรอ T-04 ตาม dependency แต่ไม่ใช่ Open Question
