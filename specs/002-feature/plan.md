# แผนการพัฒนาฟีเจอร์ยกเลิกการจองบริการ

## 1. สรุปแนวทาง
- ฟีเจอร์นี้ให้ผู้ใช้บริการยกเลิกการจองได้ตามเงื่อนไขที่กำหนดใน REQ-CMP-001 และ UC-01 โดยแยกกรณีก่อนคนขับรับงาน/หลังคนขับรับงาน/หลังเริ่มเดินทางแล้ว
- ผู้ใช้หลักคือ ลูกค้า/ผู้ใช้บริการ; ผู้ช่วยประมวลผลคือ แอดมิน และคนขับรถรับทราบผลทาง SMS
- แนวทางการสร้างคือให้มีตรวจเงื่อนไขก่อนยกเลิกในแอป แล้วคำนวณผลต่อมัดจำและส่งผลไปยัง Payment Gateway/ผู้เกี่ยวข้องตาม status
- กรณีที่เหลือเวลาไม่เกิน 120 นาที จะตัดสินเป็นริบมัดจำ ตาม AS-01 ส่วนกรณีมากกว่า 120 นาที และกรณีเริ่มงานแล้ว จะจัดเป็นบทบาทของแอดมิน/ปฏิเสธทันที ตาม AS-02 และ AS-04
- การพัฒนาควรยึดเงื่อนไขจาก spec และคงการอ้างอิงกลับไปที่ REQ-CMP-001, UC-01, AS-01 ถึง AS-06 เพื่อหลีกเลี่ยงการเพิ่มฟีเจอร์ที่ไม่ได้ระบุใน spec

## 2. เทคโนโลยีที่ใช้
| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Frontend: React + Vite + Tailwind CSS | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้เพื่อจัดการหน้าจอยกเลิกการจองและแอดมินตรวจสอบคำขอ โดยใช้ React app ที่ทำงานด้วย Vite |
| Backend: FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้เป็น API layer สำหรับ validateCancellation, cancellation-policy, refund flow, และ notification service |
| Database: PostgreSQL | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้เก็บ Booking, CancellationRequest, PaymentTransaction, NotificationMessage และ AdminAction |
| โครงสร้างโปรเจกต์เริ่มต้น | REQ-CMP-001, UC-01 | ควรเริ่มจาก โฟลเดอร์ frontend/src/, backend/app/, backend/services/, backend/models/, backend/tests/, db/init.sql, docker-compose.yml เพื่อให้ T-01 ใน tasks.md สร้างได้ตรงกัน |
| คำสั่งรัน test เริ่มต้น | ทีมเลือกเอง ไม่ได้มาจาก spec | frontend: `cd frontend && npm install && npm run test`; backend: `cd backend && python -m venv .venv && pip install -r requirements.txt && pytest`; database: `docker compose up -d postgres` |

## 3. โมเดลข้อมูล
| Entity | ฟิลด์หลัก | รองรับ spec อย่างไร |
|---|---|---|
| Booking | bookingId, customerId, driverId, appointmentTime, currentStatus, depositAmount, cancellationPolicy, createdAt | ใช้สำหรับตรวจสถานะและระยะเวลาแบบ real-time ตาม UC-01 และ AS-01 |
| CancellationRequest | requestId, bookingId, customerId, reason, requestedAt, actionBy, resultStatus, refundRate | ใช้สำหรับจัดเก็บคำร้องขอยกเลิกและผลลัพธ์จากเงื่อนไขยกเลิก ตาม REQ-CMP-001 |
| DriverStatus | driverId, tripStatus, departedAt | ใช้เพื่อกำหนดว่า “คนขับออกเดินทางแล้ว” ตาม AS-04 และ R4 |
| PaymentTransaction | bookingId, transactionId, refundAmount, referenceNo, status, processedAt | ใช้สำหรับคืนเงิน/ไม่คืนเงินตามเงื่อนไขเดียวกับ sequence flow ใน §5 |
| NotificationMessage | bookingId, recipientType, channel, sentAt, content | ใช้สำหรับ SMS แจ้งผลให้ลูกค้าและคนขับ ตาม §2 และ AS-06 |
| AdminAction | adminId, requestId, decision, reason, decidedAt | ใช้สำหรับกรณี > 120 นาที หรือกรณีต้องการตรวจสอบตาม AS-02 |

หมายเหตุ: ข้อมูล PII เช่น เบอร์โทรและข้อมูล Thai-ID จะต้องถูกเก็บตามเงื่อนไขของ §8 และไม่ควรมีฟิลด์สำเนาบัตรประชาชนเมื่อยืนยันผ่าน Thai-ID แล้ว ตามข้อจำกัดใน spec

## 4. API / หน้าจอ
| ชื่อ API / หน้า | Method / Path | Input / Output หลัก | รองรับ FR/UC |
|---|---|---|---|
| หน้ารายละเอียดการจอง | GET /bookings/{bookingId} | booking detail + cancellation policy | UC-01, REQ-CMP-001 |
| ส่งคำขอยกเลิก | POST /bookings/{bookingId}/cancel-requests | customerId, reason, requestedAt | UC-01, REQ-CMP-001 |
| ตรวจนโยบายยกเลิก | GET /bookings/{bookingId}/cancel-policy | remainingMinutes, driverStatus, depositAmount | REQ-CMP-001, AS-01, AS-04 |
| ดำเนินการยกเลิก | POST /cancel-requests/{requestId}/process | decision, refundRate, actionBy | UC-01, AS-01, AS-02 |
| ส่ง SMS แจ้งผล | POST /notifications/sms | recipientType, bookingId, status, referenceNo | §2, AS-06 |
| หน้าแอดมินจัดการยกเลิก | GET /admin/cancel-requests | list of pending requests | AS-02, AS-05 |
| อนุมัติ/ปฏิเสธยกเลิกแทนลูกค้า | PATCH /admin/cancel-requests/{requestId} | decision, reason | AS-02, AS-05 |

## 5. ตารางตรวจ Constraints
| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| REQ-CON-xxx (placeholder) | เป็นความรับผิดชอบด้าน PDPA/Thai-ID และการเก็บข้อมูลที่จำเป็นเท่านั้น | ยังไม่ได้ใช้ เพราะ spec ยังไม่มี ID ที่ชัดเจน |
| PDPA / การเก็บข้อมูล Thai-ID และที่อยู่บ้าน | ใช้เป็นเงื่อนไขในการออกแบบฟิลด์ Booking/Customer และการกำหนดสิทธิการเก็บข้อมูล | ใช้แล้ว แต่ต้องพิจารณาให้ชัดเจนต่อไป |
| ต้องเก็บหลักฐานการยืนยันตัวตนตามระยะเวลาที่กฎหมายกำหนด | ใช้ในกระบวนการแอดมินยกเลิกแทนและการยืนยันเจ้าของบัญชี | ใช้แล้วในแผน แต่ยังต้อง refine เมื่อมี ID ที่ชัด |
| ต้องไม่เก็บสำเนาบัตรประชาชนเมื่อตรวจผ่าน Thai-ID แล้ว | ใช้ในการคัดกรองฟิลด์/ข้อมูลที่ไม่เก็บใน model | ใช้แล้วในโมเดลข้อมูล |
| AS-01 ถึง AS-06 | เป็น assumption ที่ใช้กำหนด boundary 120 นาที, การภาษี/เงินที่ริบ, การแจ้ง SMS และการยืนยันเจ้าของบัญชี | ใช้แล้วในแผนเพื่อให้ logic ต่อเนื่อง |

## 6. แผนทดสอบจาก Acceptance Criteria
| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_01 | ทดสอบกรณีก่อนคนขับรับงาน: ยกเลิกแล้วคืนเงินเต็มตาม REQ-CMP-001 |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_02 | ทดสอบกรณีหลังคนขับรับงานและเหลือเวลา 120 นาที: ริบมัดจำและไม่คืนเงิน |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_03 | ทดสอบกรณีมากกว่า 120 นาที: ส่งให้แอดมินตรวจสอบและทำตามผลการตัดสิน |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_04 | ทดสอบกรณีคนขับออกเดินทางแล้ว: ปฏิเสธการยกเลิกทันที |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_05 | ทดสอบกรณีบัญชีอื่นยกเลิก: ปฏิเสธทันที |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_06 | ทดสอบส่ง SMS ให้ทั้งลูกค้าและคนขับภายใน 10 นาที ตาม AS-06 |
| AC-[ยังไม่มี ID ใน spec] | test_AC_CANCEL_07 | ทดสอบกรณี Payment Gateway คืนเงินไม่สำเร็จ: ส่ง task ให้แอดมินติดตาม |

## 7. ลำดับงาน
1. สร้าง domain model และ state logic สำหรับ Booking + CancellationRequest ตาม UC-01 และ REQ-CMP-001
2. สร้าง API ตรวจสิทธิ์และคำนวณ remainingMinutes + driverStatus ตาม AS-01 และ AS-04
3. สร้าง use case flow สำหรับกรณีก่อนรับงาน / หลังรับงาน <=120 นาที / >120 นาที / เริ่มงานแล้ว
4. สร้าง workflow สำหรับแอดมินยกเลิกแทนและยืนยันเจ้าของบัญชี ตาม AS-02 และ AS-05
5. สร้าง payment integration flow และ retry handling ในกรณีคืนเงินไม่สำเร็จ ตาม §5
6. สร้าง notification service สำหรับ SMS แจ้งผลให้ลูกค้าและคนขับ ตาม AS-06
7. สร้าง test สำหรับทุก scenario ที่ระบุใน §6 และ AS-01 ถึง AS-06
8. ตรวจสอบสิทธิ์ความเป็นส่วนตัว/PDPA และบันทึก log/traceability ให้ตรงกับ spec

## 8. สิ่งที่ยังไม่ทำ
- Q-C01: เงินมัดจำที่ไม่คืนตกเป็นของใคร — ยังไม่สามารถสร้าง policy implementation ได้จนกว่าทีมตอบชัดเจน
- Q-C02: เหลือ < 60 นาทีแต่คนขับออกเดินทางแล้ว แอดมินยกเลิกแทนได้ไหม — ยังต้องหน้างานการตัดสินใจจากทีม
- Q-C03: SMS 10 นาที ใช้กับทั้งสองฝ่ายหรือไม่ นับจากเมื่อใด — ยังไม่สร้าง trigger ที่แน่นอนจนกว่าจะได้คำตอบ
- Q-C04: ผู้รับรอง/เจ้าของ spec — ยังไม่ตอบผลการประกาศ B1 และไม่ใช่เรื่อง implement
- Q-C05: ผู้พิจารณา 60 นาที / 120 นาที และ boundary ของ time rule — ยังรอยืนยันค่า boundary จาก spec ที่ใช้งานจริง
- Q-C06: คำว่า “ค่าปรับ” กับ “ริบมัดจำ” — ยังไม่ตัดสินจากทีม จึงยังไม่สร้าง business logic ที่ยึดแนวคิดต่างกัน
- Q-C07: แอดมินยืนยันตัวตนผู้โทรอย่างไร — ยังไม่เลือก mechanism ใน implementation
- Q-C08: ยอดมัดจำคิดอย่างไร — ยังไม่สามารถกำหนด logic เชิงการเงินได้จนกว่าจะชัดเจน
- Q-C09: retry คืนเงินกี่ครั้ง ห่างเท่าไร — ยังไม่สร้าง retry policy
- Q-C10: 7 วัน นับจากเมื่อใด — ยังต้องตอบก่อนเขียนการนับเวลาเชิงการทำงาน
- Q-C11: ชื่อสถานะและ glossary — ยังไม่สามารถยืนยันชื่อ state machine สำหรับ product จริงได้
- AS-01 ถึง AS-06: เป็น assumption ที่ใช้เป็นการตัดสินใจชั่วคราว แต่ยังไม่เท่ากับความชัดเจนจากทีมอย่างเป็นทางการ

สรุป: ข้อสำคัญที่อยู่ก่อนการ implement คือ การยืนยัน boundary 120 นาที, คำถามว่าต้องมีแอดมินตอบก่อนหรือไม่, และการชี้แจงว่าเงินที่ริบเป็นของใคร เพื่อให้ logic การคืนเงินและการเก็บข้อมูลถูกต้องตาม spec
