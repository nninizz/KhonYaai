export default function App() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <div className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-brand-500">KhonYaai</p>
        <h1 className="mt-4 text-3xl font-bold text-slate-900">ยกเลิกการจองบริการ</h1>
        <p className="mt-4 text-base text-slate-600">
          ใช้สำหรับจัดการกระบวนการยกเลิกการจองตามเงื่อนไข 120 นาที, กรณีคืนเต็ม, ริบมัดจำ และการแจ้งผลให้ผู้ใช้/คนขับ
        </p>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm text-slate-500">สถานะ</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">พร้อมใช้งาน</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm text-slate-500">กรณี 120 นาที</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">ริบมัดจำ</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm text-slate-500">ผลประกาศ</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">Draft v2</p>
          </div>
        </div>
      </div>
    </main>
  );
}
