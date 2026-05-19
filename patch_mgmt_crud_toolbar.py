# -*- coding: utf-8 -*-
"""Thanh CRUD+I + phiếu xuất theo từng màn hình BQL. Chạy: python patch_mgmt_crud_toolbar.py"""
from __future__ import annotations

import html as html_module
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MODALS = """    <div id="modal-mgmt-batch-edit" class="modal-backdrop" role="dialog" aria-modal="true">
      <div class="modal modal--mgmt-crud-tip">
        <a href="#" class="modal-close" aria-label="Đóng">×</a>
        <h3>Sửa theo lựa chọn (demo)</h3>
        <p class="hint">Giao diện tĩnh: thực triển sẽ đồng bộ với checkbox trên lưới dữ liệu.</p>
        <div class="modal-actions">
          <a href="#" class="btn btn-secondary">Đóng</a>
          <a href="#" class="btn btn-primary">Tiếp tục chỉnh sửa (demo)</a>
        </div>
      </div>
    </div>
    <div id="modal-mgmt-batch-delete" class="modal-backdrop" role="dialog" aria-modal="true">
      <div class="modal modal--mgmt-crud-tip">
        <a href="#" class="modal-close" aria-label="Đóng">×</a>
        <h3>Xóa theo lựa chọn (demo)</h3>
        <p class="hint">Mockup chỉ làm động học UX — không có xóa dữ liệu thật trên máy chủ.</p>
        <div class="modal-actions">
          <a href="#" class="btn btn-secondary">Hủy</a>
          <a href="#" class="btn btn-danger">Xác nhận xóa (demo)</a>
        </div>
      </div>
    </div>
"""

HEADER_ACTIONS_RE = re.compile(
    r'<div class="mgmt-head__actions[^"]*"[^>]*>[\s\S]*?</div>',
    re.MULTILINE,
)

PHIEU_RE = re.compile(
    r'<div id="phieu-xuat-mgmt"[^>]*>[\s\S]*?</article>\s*</div>\s*',
    re.MULTILINE,
)


def _today_vn() -> str:
    return date.today().strftime("%d/%m/%Y")


def _today_compact() -> str:
    return date.today().strftime("%Y%m%d")


def make_export_sheet(
    *,
    sheet_title: str,
    rows: list[tuple[str, str]],
    amount_label: str,
    amount_value: str,
    note: str,
    ref_tag: str,
) -> str:
    """Tạo HTML phiếu xuất (id cố định #phieu-xuat-mgmt)."""
    dl_lines: list[str] = []
    for dt, dd in rows:
        dl_lines.append(
            f"          <dt>{html_module.escape(dt)}</dt>"
            f"<dd>{html_module.escape(dd)}</dd>"
        )
    dl_lines.append(f"          <dt>Thời gian xuất</dt><dd>{html_module.escape(_today_vn())}</dd>")
    dl_lines.append(
        "          <dt>Mã phiếu</dt>"
        f"<dd>{html_module.escape(f'KTX-{ref_tag}-{_today_compact()}-001')}</dd>"
    )
    dl_lines.append(
        "          <dt>Người lập phiếu</dt>"
        "<dd>Nguyễn Văn A — Cán bộ KTX (demo)</dd>"
    )
    dl_html = "\n".join(dl_lines)

    return f"""    <div id="phieu-xuat-mgmt" class="invoice-sheet-host no-print">
      <a href="#" class="invoice-sheet-scrim" aria-label="Đóng"></a>
      <article class="invoice-sheet">
        <header class="invoice-sheet__brand">
          <img src="assets/logo-dai-hoc-vinh.webp" alt="Đại học Vinh" width="56" height="56" />
          <div><h2>TRƯỜNG ĐẠI HỌC VINH</h2><p>Ban Quản lý Ký túc xá</p></div>
        </header>
        <h3 class="invoice-sheet__title">{html_module.escape(sheet_title)}</h3>
        <dl>
{dl_html}
        </dl>
        <div class="invoice-sheet__amount"><span>{html_module.escape(amount_label)}</span><strong>{html_module.escape(amount_value)}</strong></div>
        <p class="invoice-sheet__note">{html_module.escape(note)}</p>
        <footer class="invoice-sheet__foot no-print">
          <a href="#" class="btn btn-secondary btn-sm">Đóng</a>
          <button type="button" class="btn btn-primary btn-sm" onclick="window.print()">In phiếu</button>
        </footer>
      </article>
    </div>
"""


# Mỗi trang: gợi ý tooltip Xuất + nội dung phiếu riêng
PAGE_EXPORT: dict[str, dict] = {
    "quan-ly-sinh-vien.html": {
        "export_hint": "Xuất danh sách sinh viên theo bộ lọc; nhóm và lọc theo tòa · phòng đang ở (CSV/Excel demo).",
        "ref_tag": "DSSV",
        "sheet_title": "Phiếu xuất danh sách sinh viên nội trú",
        "rows": [
            ("Chức năng", "Quản lý sinh viên · UC 6.1"),
            (
                "Nội dung file xuất",
                "MSSV, họ tên, khoa, khóa, phòng đang ở, ngày đăng ký KTX, trạng thái (đang ở/đã trả/chờ duyệt), SĐT, ghi chú.",
            ),
            (
                "Phạm vi theo tòa · phòng",
                "Áp dụng bộ lọc và cột «Phòng» trên danh sách: có thể xuất theo một phòng cụ thể (vd. A-302), "
                "theo một tòa (mọi phòng có mã A-…), hoặc toàn KTX.",
            ),
            (
                "Bộ lọc đi kèm",
                "Từ khóa tìm kiếm, khoa, khóa, trạng thái — đúng như thanh công cụ phía trên bảng.",
            ),
            ("Định dạng gợi ý", "Microsoft Excel (.xlsx) · CSV UTF-8 (mẫu demo)."),
            ("Nhập ngược chiều", "Nhập CSV/Excel mẫu để bổ sung/cập nhật hàng loạt (khi triển khai backend)."),
        ],
        "amount_label": "Ước tính số dòng",
        "amount_value": "Theo số dòng đang hiển thị trên lưới (demo)",
        "note": "Phiếu minh họa — dữ liệu thật sẽ khớp bộ lọc và quyền người dùng khi có API.",
    },
    "quan-ly-phong.html": {
        "export_hint": "Xuất danh sách phòng theo tòa, loại phòng, sức chứa và trạng thái lấp đầy.",
        "ref_tag": "DSPHONG",
        "sheet_title": "Phiếu xuất danh mục phòng KTX",
        "rows": [
            ("Chức năng", "Quản lý phòng · UC 2.2"),
            (
                "Nội dung file xuất",
                "Mã phòng, tòa, tầng, loại phòng, sức chứa, số chỗ đã ở, chỗ trống, giá/tháng, trạng thái phòng.",
            ),
            (
                "Phạm vi theo tòa",
                "Lọc «Tòa» (A/B/…) kết hợp «Loại phòng» trên thanh tìm kiếm; xuất đúng tập phòng sau lọc.",
            ),
            ("Bộ lọc đi kèm", "Từ khóa số phòng, tòa, loại phòng."),
            ("Định dạng gợi ý", "Excel (.xlsx) · CSV (demo)."),
        ],
        "amount_label": "Phạm vi",
        "amount_value": "Danh sách phòng sau bộ lọc (demo)",
        "note": "Dùng cho báo cáo tồn phòng, đối chiếu với sơ đồ lấp đầy.",
    },
    "quan-ly-dang-ky.html": {
        "export_hint": "Xuất danh sách đơn đăng ký (theo phòng DK, MSSV, trạng thái duyệt).",
        "ref_tag": "DSDK",
        "sheet_title": "Phiếu xuất đơn đăng ký KTX",
        "rows": [
            ("Chức năng", "Quản lý đăng ký · UC 4.3"),
            (
                "Nội dung file xuất",
                "Mã đơn, MSSV, họ tên, phòng đăng ký mong muốn, ngày nộp, ưu tiên, trạng thái duyệt, người duyệt.",
            ),
            (
                "Phạm vi theo phòng · trạng thái",
                "Lọc theo «Phòng» và «Trạng thái» (chờ duyệt/đã duyệt/từ chối); xuất để phục vụ phê duyệt nhanh.",
            ),
            ("Định dạng gợi ý", "Excel · CSV · tổng hợp theo ngày (demo)."),
        ],
        "amount_label": "Trạng thái báo cáo",
        "amount_value": "Theo trạng thái lọc hiện tại (demo)",
        "note": "Có thể in kèm danh sách chờ duyệt gửi hội đồng KTX.",
    },
    "quan-ly-hop-dong.html": {
        "export_hint": "Xuất danh sách hợp đồng thuê (MSSV, phòng, thời hạn, trạng thái hiệu lực/thanh lý).",
        "ref_tag": "DSHD",
        "sheet_title": "Phiếu xuất danh sách hợp đồng",
        "rows": [
            ("Chức năng", "Quản lý hợp đồng · UC 4.4"),
            (
                "Nội dung file xuất",
                "Số HĐ, MSSV, họ tên, phòng, ngày bắt đầu/kết thúc, giá/tháng, tiền cọc, trạng thái, ngày thanh lý.",
            ),
            (
                "Phạm vi",
                "Theo từ khóa mã HĐ/MSSV và lọc trạng thái (hiệu lực/sắp hết hạn/đã thanh lý).",
            ),
            ("Định dạng gợi ý", "Excel (.xlsx) — kèm sheet tóm tắt theo phòng (khi triển khai)."),
        ],
        "amount_label": "Kỳ báo cáo",
        "amount_value": "Toàn bộ HĐ sau lọc (demo)",
        "note": "Phục vụ kiểm tra kỳ hạn và chuẩn bị gia hạn/thanh lý.",
    },
    "quan-ly-thanh-toan.html": {
        "export_hint": "Xuất bảng kê phiếu thu / công nợ theo kỳ tháng·năm, phòng, trạng thái thanh toán.",
        "ref_tag": "DSTT",
        "sheet_title": "Phiếu xuất danh sách thanh toán · phiếu thu",
        "rows": [
            ("Chức năng", "Quản lý thanh toán · UC 5.1"),
            (
                "Nội dung file xuất",
                "Mã phiếu, MSSV, họ tên, phòng, kỳ thu, tiền phòng, điện nước, tổng tiền, hạn TT, trạng thái, hình thức.",
            ),
            (
                "Phạm vi theo kỳ",
                "Theo «Tháng» và «Năm» đã chọn trên bộ lọc; có thể lọc thêm theo phòng hoặc trạng thái công nợ.",
            ),
            ("Định dạng gợi ý", "Excel — sheet «Tổng hợp» và «Chi tiết» (demo)."),
        ],
        "amount_label": "Tổng dư nợ (demo)",
        "amount_value": "Theo dòng «Chưa thanh toán» sau lọc",
        "note": "Đối soát trước khi chốt kỳ thu hoặc đẩy nhắc nợ qua thông báo.",
    },
    "quan-ly-thong-bao.html": {
        "export_hint": "Xuất lịch sử thông báo đã gửi (tiêu đề, đối tượng, trạng thái nháp/đã gửi).",
        "ref_tag": "DSTB",
        "sheet_title": "Phiếu xuất danh sách thông báo",
        "rows": [
            ("Chức năng", "Quản lý thông báo (BQL → sinh viên)"),
            (
                "Nội dung file xuất",
                "Ngày phát hành, tiêu đề, đối tượng nhận (toàn SV / theo tòa / nhóm phòng), trạng thái.",
            ),
            ("Bộ lọc đi kèm", "Từ khóa tiêu đề, trạng thái (đã gửi/nháp)."),
            ("Định dạng gợi ý", "Excel · CSV (demo)."),
        ],
        "amount_label": "Phạm vi",
        "amount_value": "Các tin sau bộ lọc (demo)",
        "note": "Lưu vết pháp lý và đối chiếu với cổng sinh viên.",
    },
    "quan-ly-tai-khoan.html": {
        "export_hint": "Xuất danh sách tài khoản hệ thống theo vai trò và trạng thái hoạt động.",
        "ref_tag": "DSTK",
        "sheet_title": "Phiếu xuất danh sách người dùng · tài khoản",
        "rows": [
            ("Chức năng", "Quản lý tài khoản · UC 1.1 / 1.3 / 1.4"),
            (
                "Nội dung file xuất",
                "Tên đăng nhập, họ tên, vai trò (quản trị/cán bộ/SV), trạng thái, email/liên hệ (khi có).",
            ),
            ("Bộ lọc đi kèm", "Theo vai trò và «Hoạt động/Đã khóa»."),
            ("Định dạng gợi ý", "Excel — ẩn cột nhạy cảm khi export (thiết kế bảo mật)."),
        ],
        "amount_label": "Cảnh báo",
        "amount_value": "Chỉ dùng nội bộ Bộ phận CNTT / BQL được ủy quyền",
        "note": "Kèm Audit log khi có hệ thống thật.",
    },
    "vat-tu-phong.html": {
        "export_hint": "Xuất kiểm kê vật tư phòng (theo mã VT, phòng, số lượng, tình trạng).",
        "ref_tag": "DSVT",
        "sheet_title": "Phiếu xuất kiểm kê vật tư phòng",
        "rows": [
            ("Chức năng", "Quản lý vật tư phòng · UC 3.1 · UC 3.2"),
            (
                "Nội dung file xuất",
                "Mã vật tư, tên, phòng đặt VT, số lượng, tình trạng (tốt/hỏng/đang sửa), ngày cập nhật.",
            ),
            ("Phạm vi theo phòng", "Lọc «Phòng» hoặc xuất toàn KTX để báo hỏng và mua sắm bổ sung."),
            ("Định dạng gợi ý", "Excel (.xlsx) — nhóm Sheet theo tòa/phòng (khi triển khai)."),
        ],
        "amount_label": "Mục đích",
        "amount_value": "Báo cáo bảo trì · đối soát tài sản",
        "note": "Có thể in phiếu giao nhận kèm chữ ký BQL.",
    },
    "toa-nha.html": {
        "export_hint": "Xuất danh mục tòa nhà (mã, tên, số tầng, tổng phòng, số SV đang ở).",
        "ref_tag": "DSTOA",
        "sheet_title": "Phiếu xuất danh mục tòa nhà",
        "rows": [
            ("Chức năng", "Quản lý tòa nhà · UC 2.1"),
            (
                "Nội dung file xuất",
                "Mã tòa, tên hiển thị, số tầng, tổng phòng, số sinh viên đang ở (tổng hợp).",
            ),
            ("Bộ lọc đi kèm", "Từ khóa tìm theo tên hoặc mã tòa."),
            ("Định dạng gợi ý", "Excel · PDF bảng tóm tắt (demo)."),
        ],
        "amount_label": "Phạm vi",
        "amount_value": "Toàn danh mục tòa hiện có (demo)",
        "note": "Là master data trước khi thêm phòng vào từng tòa.",
    },
    "thiet-lap-phong.html": {
        "export_hint": "Xuất cấu hình phòng KTX đang thiết lập (theo tòa, loại, giá, sức chứa).",
        "ref_tag": "DSPHCFG",
        "sheet_title": "Phiếu xuất cấu hình · thiết lập phòng KTX",
        "rows": [
            ("Chức năng", "Thiết lập phòng · UC 2.2"),
            (
                "Nội dung file xuất",
                "Phòng, tòa, loại giường/phòng, sức chứa quy định, đơn giá theo học kỳ·tháng (theo mockup hiện tại).",
            ),
            ("Phạm vi theo tòa", "Lọc «Tòa» + «Loại phòng» trên thanh công cụ."),
            ("Định dạng gợi ý", "Excel — dùng làm mẫu import hàng loạt khi mở đợt KTX mới."),
        ],
        "amount_label": "Ghi chú",
        "amount_value": "Khớp với «Quản lý phòng» sau khi duyệt cấu hình",
        "note": "Khác trang «Quản lý phòng» ở chỗ tập trung thiết lập giá và quy tắc trước khi vận hành.",
    },
    "ho-so-noi-tru.html": {
        "export_hint": "Xuất danh sách hồ sơ nội trú theo MSSV, phòng và lớp (Excel/CSV demo).",
        "ref_tag": "DSHSNT",
        "sheet_title": "Phiếu xuất danh sách hồ sơ nội trú",
        "rows": [
            ("Chức năng", "Hồ sơ nội trú · UC 6.1 — vận hành & tra cứu"),
            (
                "Nội dung file xuất",
                "MSSV, họ tên, lớp/ghi nhận khóa, phòng và tòa, giường, ngày vào ở, ngày hết hạn hồ sơ/HĐ gắn kèm, trạng thái đang nội trú, "
                "SĐT, liên hệ khẩn, ghi chú BQL.",
            ),
            (
                "Phạm vi · bộ lọc",
                "Theo kết quả tìm MSSV và lọc phòng · lớp trên form — xuất đúng các dòng đang hiển thị sau lọc.",
            ),
            ("Định dạng gợi ý", "Excel (.xlsx) · CSV UTF-8 (demo)."),
            ("Nhập ngược chiều", "Mẫu CSV đối chiếu với cổng sinh viên khi có API đồng bộ."),
        ],
        "amount_label": "Số lượng bản ghi",
        "amount_value": "Giống tổng dòng trong bảng sau lọc (demo)",
        "note": "Hồ sơ nội trú trong mockup chỉ là tầng nhìn danh mục; master SV đầy đủ có thể mở từ Quản lý sinh viên.",
    },
}

PAGES: list[tuple[str, str, str]] = [
    ("ho-so-noi-tru.html", "#drawer-them-hoso", "+ Thêm hồ sơ nội trú"),
    ("quan-ly-sinh-vien.html", "#drawer-them-sv", "+ Thêm sinh viên"),
    ("quan-ly-phong.html", "#drawer-them-phong", "+ Thêm phòng"),
    ("quan-ly-dang-ky.html", "#drawer-dk-detail", "+ Thêm đơn (form chi tiết)"),
    ("quan-ly-hop-dong.html", "#drawer-hd-detail", "+ Thêm hợp đồng (form chi tiết)"),
    ("quan-ly-thanh-toan.html", "#drawer-tt-detail", "+ Ghi nhận thanh toán"),
    ("quan-ly-thong-bao.html", "#drawer-dang-thong-bao", "+ Đăng thông báo"),
    ("quan-ly-tai-khoan.html", "#modal-add-user", "+ Thêm tài khoản"),
    ("vat-tu-phong.html", "#drawer-them-vattu", "+ Thêm vật tư"),
    ("toa-nha.html", "#drawer-them-toa", "+ Thêm tòa nhà"),
    ("thiet-lap-phong.html", "#drawer-them-phong", "+ Thêm phòng"),
]


def make_toolbar(add_href: str, add_label: str, export_hint: str) -> str:
    title_attr = ""
    if export_hint.strip():
        title_attr = ' title="%s"' % html_module.escape(export_hint, quote=True)

    return f"""              <div class="mgmt-head__actions mgmt-crud-toolbar" role="toolbar" aria-label="Thêm sửa xóa nhập xuất">
                <a href="{html_module.escape(add_href, quote=True)}" class="btn-mgmt-primary mgmt-crud-toolbar__primary">{html_module.escape(add_label)}</a>
                <a href="#modal-mgmt-batch-edit" class="btn-mgmt-outline mgmt-crud-toolbar__edit">Sửa</a>
                <a href="#modal-mgmt-batch-delete" class="btn-mgmt-outline mgmt-crud-toolbar__danger">Xóa</a>
                <a href="#phieu-xuat-mgmt" class="btn-mgmt-outline mgmt-crud-toolbar__export"{title_attr}>Xuất</a>
                <label class="btn-mgmt-outline mgmt-crud-toolbar__import">
                  Nhập
                  <input type="file" accept=".csv,.xlsx,.xls" aria-label="Nhập từ file (demo)" />
                </label>
              </div>"""


def merge_modals_and_sheet(html: str, sheet_html: str) -> str:
    if 'id="modal-mgmt-batch-edit"' not in html and "</body>" in html:
        html = html.replace("</body>", MODALS + "\n</body>", 1)
    m = PHIEU_RE.search(html)
    if m:
        html = html[: m.start()] + sheet_html + "\n" + html[m.end() :]
    elif "</body>" in html:
        html = html.replace("</body>", sheet_html + "\n</body>", 1)
    return html


def patch_file(rel: str, href: str, label: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    meta = PAGE_EXPORT.get(rel)
    if not meta:
        raise SystemExit(f"Thiếu PAGE_EXPORT cho {rel}")

    export_hint = meta["export_hint"]
    repl = make_toolbar(href, label, export_hint)
    text2, n = HEADER_ACTIONS_RE.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit(f"{rel}: không tìm thấy mgmt-head__actions (thay được {n} lần)")

    sheet = make_export_sheet(
        sheet_title=meta["sheet_title"],
        rows=meta["rows"],
        amount_label=meta["amount_label"],
        amount_value=meta["amount_value"],
        note=meta["note"],
        ref_tag=meta["ref_tag"],
    )
    text3 = merge_modals_and_sheet(text2, sheet)
    path.write_text(text3, encoding="utf-8")


def main() -> None:
    for rel, h, lab in PAGES:
        patch_file(rel, h, lab)
        print("OK", rel)


if __name__ == "__main__":
    main()
