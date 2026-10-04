# prompt-log.md บันทึกการใช้ AI ของกลุ่ม <ชื่อกลุ่ม>

กติกา: เพิ่มต่อท้ายเท่านั้น ห้ามแก้หรือลบบันทึกเดิม
ทุกบันทึกมี: เลขที่ | วันที่ | เครื่องมือ | คำสั่ง | สิ่งที่ AI ถามหรือรายงาน | คำตอบหรือการตัดสินใจของทีม | สิ่งที่ AI เดา (ถ้ามี)
AI จะเพิ่มบันทึกให้เองเมื่อใช้คำสั่ง /clarify /plan /tasks /implement ทีมเพิ่มเองได้เมื่อสั่งแก้นอกคำสั่ง

## #2 | 2569-10-04 | copilot | /clarify specs/002-feature/spec.md
| ทีมตั้งคำถามเรื่อง boundary 120 นาที, การริบมัดจำ, การยืนยันเจ้าของบัญชีและการนับเวลา | ใช้ค่าเดิมตามที่ AI เดา: 120 นาทีถือว่าเป็นกรณีริบมัดจำ; >120 นาทีให้แอดมินตรวจสอบ; เงินที่ริบเป็นทรัพย์แพลตฟอร์ม; ใช้สถานะ “ออกเดินทางแล้ว” เป็นเกณฑ์ปฏิเสธ; แอดมินต้องยืนยันเจ้าของบัญชี; นับเวลาเริ่มจากบันทึกผล | AI เดา: 120 นาที = <= 120 นาที, เงินที่ริบเป็นทรัพย์แพลตฟอร์ม, driver departed = status เดินทางแล้ว, n = from record result

## #3 | 2569-10-04 | copilot | /plan specs/002-feature/spec.md
| สร้าง plan.md จาก spec.md และคงสภาพที่ยังไม่ชัดในด้านเทคโนโลยี/ID/การอ้างอิง constraint ให้ชัดว่าเป็น pending | plan.md ถูกสร้างแล้วในโฟลเดอร์เดียวกับ spec โดยยึด REQ-CMP-001, UC-01, AS-01 ถึง AS-06 เป็นหลัก และระบุว่าเทคโนโลยี/stack ยังต้องรอทีมเลือก | AI สรุปว่ามี open questions หลายข้อที่ยังไม่พร้อมสำหรับ implement และจึงคงไว้เป็นสิ่งที่ยังไม่ทำใน plan.md

## #4 | 2569-10-04 | copilot | /tasks specs/002-feature/spec.md
| แตก plan.md เป็น tasks.md โดยยึดโครง model → business logic → API → admin/payment → tests และคง task ที่รอคำตอบจากทีมไว้เป็น status รอ Q-xx | tasks.md ถูกสร้างในโฟลเดอร์เดียวกับ spec พร้อมสรุป 7 task, 3 task ที่ต้องรอคำตอบจากทีม และตารางตรวจความครบทั้ง AC และ Constraint | AI จัด task เป็นลำดับพึ่งพากันและยืนยันว่ายังไม่เริ่ม implement จริง จนกว่าทีมจะสั่งต่อ

## #5 | 2569-10-04 | copilot | /edit-stack specs/002-feature/spec.md
| ทีมสั่งให้ปรับ spec/plan/tasks ให้ใช้ React + Vite + Tailwind ใน frontend, FastAPI ใน backend, PostgreSQL ใน database | ทุกไฟล์ที่เกี่ยวข้องปรับให้สะท้อน stack ใหม่ และระบุว่าเป็น “ทีมเลือกเอง ไม่ได้มาจาก spec” เพื่อให้สอดคล้องกับกฎ traceability | AI ปรับ [specs/002-feature/spec.md](specs/002-feature/spec.md), [specs/002-feature/plan.md](specs/002-feature/plan.md), [specs/002-feature/tasks.md](specs/002-feature/tasks.md) และบันทึกคำตัดสินใจนี้ต่อท้าย prompt-log.md

## #6 | 2569-10-04 | copilot | /implement T-01 specs/002-feature/tasks.md
| ทำ task T-01 เฉพาะโครงโปรเจกต์และ smoke test bootstrap ตามไฟล์ที่แตะ | สร้าง frontend React + Vite + Tailwind scaffolding, backend FastAPI hello-health API, PostgreSQL init SQL และ docker-compose; รัน frontend build และ backend pytest smoke test | ผล test: frontend build สำเร็จ; backend smoke test ผ่าน 1 test; T-01 ถูกเปลี่ยนสถานะเป็น “เสร็จ รอทีมตรวจ”

## #7 | 2569-10-04 | copilot | /implement T-02 specs/002-feature/tasks.md
| ทำ task T-02 เฉพาะ model ของการจอง/คำขอยกเลิกและ driver status ให้สอดคล้องกับ flow ยกเลิกที่กำหนด | สร้าง backend/models/booking.py, backend/models/cancellation_request.py, backend/models/driver_status.py และปรับ db/init.sql ให้มีตาราง driver_status พร้อม field ที่ต้องใช้; ตรวจสอบด้วยโค้ดจริงว่า remaining_minutes = 90 นาที, is_within_cancellation_window <= 120 นาที, และ driver_status.is_departed() ทำงาน | ผล validation: PYTHONPATH=. python3 ... => "model validation passed"; T-02 ถูกเปลี่ยนสถานะเป็น “เสร็จ รอทีมตรวจ”

## #8 | 2569-10-04 | copilot | /clarify specs/002-feature/spec.md
| รายงานความกำกวมใน REQ-CMP-001, UC-01, R1-R4, §5-§8 และถามคำถาม 8 ข้อที่กระทบการวางแผน | ทีมตอบว่า “เอาตามนั้นเลย” หมายถึงยอมรับข้อสรุปที่เสนอทั้งหมด: รองรับก่อน/หลังคนขับรับงาน, กรณี >120 นาทีรอแอดมิน, เงินที่ริบเป็นของแพลตฟอร์ม, สถานะออกเดินทางมีสิทธิ์ปฏิเสธสูงสุด, SMS ส่งทั้งสองฝ่ายภายใน 10 นาที และริบมัดจำ 100% ถือเป็นค่าปรับ | ปรับ spec.md ให้ชัดเจนและเพิ่ม ASM-01 ถึง ASM-08; ไม่สร้าง ID ใหม่ของ requirement/AC และไม่แก้โค้ดหรือแผนงาน

## #9 | 2569-10-04 | copilot | /tasks specs/002-feature/spec.md
| ทบทวน tasks.md หลังทีมตอบข้อกำกวมจากการ clarify | แก้รอบที่ 2: เปลี่ยน T-03, T-05 และ T-06 จาก “รอ Q-xx” เป็น “พร้อมทำ”, ปรับสรุปเป็นไม่มี task ที่รอ Open Questions และระบุว่า T-05/T-06 ยังมี dependency ที่ต้องทำหลัง T-04 | เหตุผล: Q ที่เกี่ยวข้องถูกตัดสินและบันทึกใน spec.md แล้ว; ไม่เพิ่ม task และยังไม่เริ่ม implement task ใด

## #10 | 2569-10-04 | copilot | /implement T-03 specs/002-feature/tasks.md
| ทำ T-03 เฉพาะ engine นโยบายยกเลิกและตัวประเมินสถานะการจองตาม REQ-CMP-001, R2, R3, R4, AS-01 และ AS-04 | สร้าง backend/services/cancellation_policy.py และ backend/services/booking_status_evaluator.py; รองรับคืนเต็ม, ริบมัดจำเมื่อเวลาเหลือ <= 120 นาที, ส่งแอดมินตรวจสอบเมื่อ >120 นาที และปฏิเสธเมื่อสถานะไม่อนุญาต/คนขับออกเดินทางแล้ว | ผล test inline: test_AC_CANCEL_01 ถึง test_AC_CANCEL_05 ผ่านทั้งหมด; ไม่มีสิ่งที่ต้องเดาเพิ่มเพราะใช้ status_allows_cancellation เป็นข้อมูลจากผู้เรียกตาม spec; T-03 เปลี่ยนเป็น “เสร็จ รอทีมตรวจ”
