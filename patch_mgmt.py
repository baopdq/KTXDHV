# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TAG = re.compile(r"</?motion[^>]*>")


def scrub(s):
    return TAG.sub("", s)


def row_actions(drawer):
    v = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>'
    e = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" /></svg>'
    d = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>'
    return (
        f'<div class="table-bql-actions table-bql-actions--tight">'
        f'<a href="{drawer}" class="icon-btn-mgmt icon-btn-mgmt--view" title="Xem" aria-label="Xem">{v}</a>'
        f'<a href="{drawer}" class="icon-btn-mgmt icon-btn-mgmt--edit" title="Sửa" aria-label="Sửa">{e}</a>'
        f'<button type="button" class="icon-btn-mgmt icon-btn-mgmt--danger" title="Xóa (demo)" aria-label="Xóa">{d}</button>'
        f"</div>"
    )


SV_ROWS = [
    ("1", "221001", "Nguyễn Văn An", "CNTT", "K62", "A-302", "01/09/2024", "success", "Đang ở"),
    ("2", "221002", "Trần Thị Bình", "QTKD", "K62", "A-302", "05/09/2024", "success", "Đang ở"),
    ("3", "221045", "Lê Văn Cường", "Điện", "K63", "B-105", "10/09/2024", "warning", "Chờ duyệt"),
    ("4", "221088", "Phạm Thị Dung", "Kế toán", "K61", "B-105", "12/08/2024", "muted", "Đã trả"),
    ("5", "221112", "Hoàng Văn Em", "CNTT", "K62", "A-401", "20/09/2024", "success", "Đang ở"),
    ("6", "221156", "Võ Thị Phương", "Ngữ văn", "K62", "C-118", "22/09/2024", "warning", "Chờ duyệt"),
    ("7", "221203", "Đặng Văn Giang", "Cơ khí", "K63", "B-210", "25/09/2024", "success", "Đang ở"),
]

THEM_SV = """
    <div id="drawer-them-sv" class="mgmt-drawer-host">
      <a href="#" class="mgmt-drawer-scrim" aria-label="Đóng"></a>
      <aside class="mgmt-drawer-panel mgmt-drawer-panel--wide" role="dialog" aria-labelledby="them-sv-title" aria-modal="true">
        <div class="mgmt-drawer-head"><h2 id="them-sv-title">Thêm sinh viên</h2><a href="#" class="mgmt-drawer-close" aria-label="Đóng">×</a></div>
        <div class="mgmt-drawer-body">
          <form>
            <div class="form-group"><label>Mã sinh viên *</label><input required placeholder="221xxx" /></div>
            <div class="form-group"><label>Họ và tên *</label><input required /></div>
            <div class="form-group"><label>Ngày sinh *</label><input type="date" required /></div>
            <div class="form-group"><label>Giới tính *</label><select required><option>Nam</option><option>Nữ</option></select></div>
            <div class="form-group"><label>Số điện thoại *</label><input required /></div>
            <div class="form-group"><label>Email *</label><input type="email" required /></div>
            <div class="form-group"><label>Khoa *</label><select required><option>CNTT</option><option>QTKD</option></select></div>
            <div class="form-group"><label>Khóa *</label><input required placeholder="2021" /></div>
            <div class="form-group"><label>Lớp *</label><input required /></div>
            <div class="form-group"><label>Quê quán</label><input /></div>
            <motion></motion>
            <div class="form-group"><label>CMND/CCCD *</label><input required /></div>
            <div class="form-group"><label>Địa chỉ thường trú *</label><textarea rows="2" required></textarea></div>
            <div class="form-group"><label>Trạng thái *</label><select required><option>Chờ duyệt</option><option>Đang ở</option></select></div>
          </form>
        </div>
        <div class="mgmt-drawer-foot"><div style="display:flex;gap:8px"><a href="#" class="btn-mgmt-outline" style="flex:1;justify-content:center">Hủy</a><button type="button" class="btn-mgmt-block btn-mgmt-block--blue" style="flex:1">Lưu (demo)</button></div></div>
      </aside>
    </div>
"""


def patch_sinh_vien():
    path = ROOT / "quan-ly-sinh-vien.html"
    html = scrub(path.read_text(encoding="utf-8"))
    drawer = scrub((ROOT / "partials" / "drawer-sv-detail.html").read_text(encoding="utf-8"))
    rows = []
    for stt, mssv, name, khoa, khoa_y, room, date, badge, status in SV_ROWS:
        rows.append(
            "                        <tr>\n"
            f'                          <td data-label="STT">{stt}</td>\n'
            f'                          <td data-label="Mã SV">{mssv}</td>\n'
            f'                          <td data-label="Họ tên">{name}</td>\n'
            f'                          <td data-label="Khoa">{khoa}</td>\n'
            f'                          <td data-label="Khóa">{khoa_y}</td>\n'
            f'                          <td data-label="Phòng">{room}</td>\n'
            f'                          <td data-label="Ngày ĐK">{date}</td>\n'
            f'                          <td data-label="TT"><span class="badge-bql badge-bql--{badge}">{status}</span></td>\n'
            f'                          <td data-label="Thao tác">{row_actions("#drawer-sv-detail")}</td>\n'
            "                        </tr>"
        )
    html = re.sub(
        r"<tbody>[\s\S]*?</tbody>",
        "<tbody>\n" + "\n".join(rows) + "\n                      </tbody>",
        html,
        count=1,
    )
    html = re.sub(
        r'    <div id="drawer-[^"]+" class="mgmt-drawer-host">[\s\S]*?(?=    </body>)',
        scrub(drawer) + scrub(THEM_SV),
        html,
        count=1,
    )
    if "+ Thêm sinh viên" not in html:
        html = html.replace(
            '<div class="mgmt-head__actions">\n                <button type="button" class="btn-mgmt-outline">Xuất Excel',
            '<div class="mgmt-head__actions">\n                <a href="#drawer-them-sv" class="btn-mgmt-primary">+ Thêm sinh viên</a>\n                <button type="button" class="btn-mgmt-outline">Xuất Excel',
        )
    path.write_text(scrub(html), encoding="utf-8")
    print("patched", path.name)


def dl_section(title, pairs):
    items = "\n".join(f"              <motion></motion><div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pairs)
    items = "\n".join(f"              <div><dt>{k}</dt><dd>{v}</dd></motion></motion>" for k, v in pairs)
    items = scrub("\n".join(f"              <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pairs))
    return f"""
          <section class="mgmt-drawer-section">
            <h3>{title}</h3>
            <dl class="mgmt-dl mgmt-dl--grid">
{items}
            </dl>
          </section>"""


def drawer_simple(drawer_id, title, sections, foot_extra=""):
    body = "".join(dl_section(h, fields) for h, fields in sections)
    foot = '<button type="button" class="btn-mgmt-block btn-mgmt-block--blue">Cập nhật (demo)</button>'
    if foot_extra:
        foot += foot_extra
    return scrub(f"""
    <div id="{drawer_id}" class="mgmt-drawer-host">
      <a href="#" class="mgmt-drawer-scrim" aria-label="Đóng"></a>
      <aside class="mgmt-drawer-panel mgmt-drawer-panel--wide" role="dialog" aria-labelledby="{drawer_id}-title" aria-modal="true">
        <div class="mgmt-drawer-head">
          <h2 id="{drawer_id}-title">{title}</h2>
          <a href="#" class="mgmt-drawer-close" aria-label="Đóng">×</a>
        </div>
        <div class="mgmt-drawer-body">{body}
        </div>
        <div class="mgmt-drawer-foot">{foot}</div>
      </aside>
    </div>""")


def patch_page(filename, title, breadcrumb, h1, sub, thead, rows_html, drawer_html, head_btn=""):
    path = ROOT / filename
    html = scrub(path.read_text(encoding="utf-8"))
    html = re.sub(r"<title>[^<]+</title>", f"<title>{title} — KTX Đại học Vinh</title>", html, count=1)
    html = re.sub(
        r'<nav class="mgmt-breadcrumb"[^>]*>[\s\S]*?</nav>',
        f'<nav class="mgmt-breadcrumb" aria-label="Breadcrumb"><a href="tong-quan.html">Trang chủ</a><span class="sep">/</span><span>{breadcrumb}</span></nav>',
        html,
        count=1,
    )
    html = re.sub(r"<h1 class=\"page-title\">[^<]+</h1>", f"<h1 class=\"page-title\">{h1}</h1>", html, count=1)
    html = re.sub(r"<p class=\"mgmt-sub\">[\s\S]*?</p>", f"<p class=\"mgmt-sub\">{sub}</p>", html, count=1)
    if thead and "<thead>" in html:
        html = re.sub(r"<thead>[\s\S]*?</thead>", thead, html, count=1)
    if rows_html:
        html = re.sub(r"<tbody>[\s\S]*?</tbody>", f"<tbody>\n{rows_html}\n                      </tbody>", html, count=1)
    if drawer_html:
        html = re.sub(
            r'    <div id="drawer-[^"]+" class="mgmt-drawer-host">[\s\S]*?(?=    </body>)',
            drawer_html,
            html,
            count=1,
        )
        html = re.sub(r'    <div id="modal-[^"]+"[\s\S]*?(?=    </body>)', drawer_html, html, count=0)
    if head_btn and head_btn not in html:
        html = html.replace(
            '<div class="mgmt-head__actions">',
            f'<div class="mgmt-head__actions">{head_btn}',
            1,
        )
    path.write_text(scrub(html), encoding="utf-8")
    print("patched", filename)


def patch_phong():
    thead = """<thead>
                        <tr>
                          <th>STT</th><th>Mã phòng</th><th>Tòa</th><th>Tầng</th><th>Loại</th>
                          <th>Sức chứa</th><th>Đã ở</th><th>Trống</th><th>Giá/tháng</th><th>Trạng thái</th><th>Chức năng</th>
                        </tr>
                      </thead>"""
    rows = []
    data = [
        ("1", "A-302", "A", "3", "Tiêu chuẩn", "4", "4", "0", "350.000", "success", "Đang sử dụng"),
        ("2", "A-401", "A", "4", "Tiêu chuẩn", "4", "3", "1", "350.000", "success", "Đang sử dụng"),
        ("3", "B-105", "B", "1", "VIP", "2", "2", "0", "500.000", "success", "Đang sử dụng"),
        ("4", "B-210", "B", "2", "Tiêu chuẩn", "4", "2", "2", "350.000", "warning", "Bảo trì"),
        ("5", "C-118", "C", "1", "Tiêu chuẩn", "4", "1", "3", "320.000", "success", "Đang sử dụng"),
    ]
    for stt, ma, toa, tang, loai, suc, o, trong, gia, badge, tt in data:
        rows.append(
            f"                        <tr><td>{stt}</td><td>{ma}</td><td>{toa}</td><td>{tang}</td><td>{loai}</td>"
            f"<td>{suc}</td><td>{o}</td><td>{trong}</td><td>{gia} ₫</td>"
            f'<td><span class="badge-bql badge-bql--{badge}">{tt}</span></td>'
            f'<td>{row_actions("#drawer-phong-detail")}</td></tr>'
        )
    drawer = drawer_simple("drawer-phong-detail", "Chi tiết phòng", [
        ("Thông tin phòng", [
            ("Mã phòng", "A-302"), ("Tòa", "Tòa A"), ("Tầng", "3"), ("Loại phòng", "Tiêu chuẩn 4 người"),
            ("Diện tích", "28 m²"), ("Sức chứa", "4 giường"), ("Đã ở", "4"), ("Còn trống", "0"),
            ("Giá phòng/tháng", "350.000 ₫"), ("Tiền điện", "Theo đồng hồ"), ("Tiền nước", "20.000 ₫/người"),
            ("Trạng thái", "Đang sử dụng"), ("Ngày thiết lập", "15/08/2023"), ("Ghi chú", "Có máy lạnh"),
        ]),
    ])
    patch_page(
        "quan-ly-phong.html",
        "Quản lý phòng",
        "Quản lý phòng",
        "Quản lý phòng",
        "<code>UC 2.2</code> — Danh mục phòng, sức chứa và trạng thái lấp đầy.",
        thead,
        "\n".join(rows),
        drawer,
        '<a href="#drawer-them-phong" class="btn-mgmt-primary">+ Thêm phòng</a>',
    )


def patch_dang_ky():
    thead = """<thead><tr>
      <th>STT</th><th>Mã đơn</th><th>MSSV</th><th>Họ tên</th><th>Phòng DK</th>
      <th>Ngày nộp</th><th>Ưu tiên</th><th>Trạng thái</th><th>Chức năng</th>
    </tr></thead>"""
    rows = []
    data = [
        ("1", "DK-2401", "221045", "Lê Văn Cường", "A-302", "10/05/2026", "Có", "warning", "Chờ duyệt"),
        ("2", "DK-2402", "221112", "Hoàng Văn Em", "B-105", "11/05/2026", "Không", "warning", "Chờ duyệt"),
        ("3", "DK-2398", "221203", "Đặng Văn Giang", "A-401", "08/05/2026", "Không", "success", "Đã duyệt"),
        ("4", "DK-2390", "221088", "Phạm Thị Dung", "B-210", "01/05/2026", "Có", "muted", "Đã từ chối"),
    ]
    for stt, ma, mssv, ten, phong, ngay, uu, badge, tt in data:
        rows.append(
            f"<tr><td>{stt}</td><td>{ma}</td><td>{mssv}</td><td>{ten}</td><td>{phong}</td><td>{ngay}</td><td>{uu}</td>"
            f'<td><span class="badge-bql badge-bql--{badge}">{tt}</span></td><td>{row_actions("#drawer-dk-detail")}</td></tr>'
        )
    drawer = drawer_simple("drawer-dk-detail", "Chi tiết đơn đăng ký", [
        ("Thông tin đơn", [
            ("Mã đơn", "DK-2401"), ("MSSV", "221045"), ("Họ tên", "Lê Văn Cường"), ("Khoa", "Điện — Kỹ thuật"),
            ("Khóa", "K63"), ("Lớp", "ĐT63A"), ("Phòng đăng ký", "A-302"), ("Ngày nộp", "10/05/2026 14:32"),
            ("Loại đăng ký", "Nội trú học kỳ II"), ("Minh chứng ưu tiên", "Hộ nghèo — đã nộp"),
            ("Trạng thái", "Chờ duyệt"), ("Người duyệt", "—"), ("Ngày duyệt", "—"), ("Lý do từ chối", "—"),
        ]),
    ], '<a href="#" class="btn-bql btn-bql-primary" style="margin-top:8px">Duyệt (demo)</a>')
    patch_page(
        "quan-ly-dang-ky.html",
        "Quản lý đăng ký",
        "Quản lý đăng ký",
        "Quản lý đăng ký",
        "<code>UC 4.3</code> — Tiếp nhận, duyệt và theo dõi đơn đăng ký ở KTX.",
        thead,
        "\n".join(rows),
        drawer,
    )


def patch_hop_dong():
    thead = """<thead><tr>
      <th>STT</th><th>Số HĐ</th><th>MSSV</th><th>Họ tên</th><th>Phòng</th>
      <th>Bắt đầu</th><th>Kết thúc</th><th>Giá/tháng</th><th>Trạng thái</th><th>Chức năng</th>
    </tr></thead>"""
    rows = []
    data = [
        ("1", "HD-2024-0892", "221001", "Nguyễn Văn An", "A-302", "01/09/2024", "31/08/2025", "350.000", "success", "Hiệu lực"),
        ("2", "HD-2024-0901", "221002", "Trần Thị Bình", "A-302", "01/09/2024", "31/08/2025", "350.000", "success", "Hiệu lực"),
        ("3", "HD-2023-0440", "221088", "Phạm Thị Dung", "B-105", "01/09/2023", "15/08/2024", "350.000", "muted", "Đã thanh lý"),
    ]
    for stt, so, mssv, ten, phong, bd, kt, gia, badge, tt in data:
        rows.append(
            f"<tr><td>{stt}</td><td>{so}</td><td>{mssv}</td><td>{ten}</td><td>{phong}</td><td>{bd}</td><td>{kt}</td>"
            f"<td>{gia} ₫</td><td><span class=\"badge-bql badge-bql--{badge}\">{tt}</span></td>"
            f"<td>{row_actions('#drawer-hd-detail')}</td></tr>"
        )
    drawer = drawer_simple("drawer-hd-detail", "Chi tiết hợp đồng", [
        ("Hợp đồng thuê phòng", [
            ("Số hợp đồng", "HD-2024-0892"), ("MSSV", "221001"), ("Họ tên", "Nguyễn Văn An"),
            ("Phòng", "A-302 — Giường 2"), ("Ngày bắt đầu", "01/09/2024"), ("Ngày kết thúc", "31/08/2025"),
            ("Giá thuê/tháng", "350.000 ₫"), ("Tiền cọc", "700.000 ₫"), ("Chu kỳ thanh toán", "Theo tháng"),
            ("Trạng thái", "Hiệu lực"), ("Ngày ký", "28/08/2024"), ("File đính kèm", "HD-2024-0892.pdf"),
            ("Ngày thanh lý", "—"), ("Ghi chú", "Gia hạn tự động nếu không báo trả phòng"),
        ]),
    ], '<button type="button" class="btn-mgmt-block btn-mgmt-block--danger">Thanh lý (demo)</button>')
    patch_page(
        "quan-ly-hop-dong.html",
        "Quản lý hợp đồng",
        "Quản lý hợp đồng",
        "Quản lý hợp đồng",
        "<code>UC 4.4</code> — Lập, gia hạn và thanh lý hợp đồng thuê phòng.",
        thead,
        "\n".join(rows),
        drawer,
    )


def patch_thanh_toan():
    thead = """<thead><tr>
      <th>STT</th><th>Mã phiếu</th><th>MSSV</th><th>Họ tên</th><th>Phòng</th>
      <th>Kỳ thu</th><th>Tổng tiền</th><th>Hạn TT</th><th>Trạng thái</th><th>Chức năng</th>
    </tr></thead>"""
    rows = []
    data = [
        ("1", "PT-0526-001", "221001", "Nguyễn Văn An", "A-302", "05/2026", "1.420.000", "25/05/2026", "warning", "Chưa thanh toán"),
        ("2", "PT-0526-002", "221002", "Trần Thị Bình", "A-302", "05/2026", "1.420.000", "25/05/2026", "success", "Đã thanh toán"),
        ("3", "PT-0426-001", "221001", "Nguyễn Văn An", "A-302", "04/2026", "1.400.000", "25/04/2026", "success", "Đã thanh toán"),
    ]
    for stt, ma, mssv, ten, phong, ky, tong, han, badge, tt in data:
        rows.append(
            f"<tr><td>{stt}</td><td>{ma}</td><td>{mssv}</td><td>{ten}</td><td>{phong}</td><td>{ky}</td>"
            f"<td>{tong} ₫</td><td>{han}</td><td><span class=\"badge-bql badge-bql--{badge}\">{tt}</span></td>"
            f"<td>{row_actions('#drawer-tt-detail')}</td></tr>"
        )
    drawer = drawer_simple("drawer-tt-detail", "Chi tiết thanh toán", [
        ("Hóa đơn / phiếu thu", [
            ("Mã phiếu thu", "PT-0526-001"), ("Số hợp đồng", "HD-2024-0892"), ("MSSV", "221001"),
            ("Họ tên", "Nguyễn Văn An"), ("Phòng", "A-302"), ("Kỳ thu", "05/2026"),
            ("Từ ngày", "01/05/2026"), ("Đến ngày", "31/05/2026"), ("Tiền phòng", "1.400.000 ₫"),
            ("Phí dịch vụ", "20.000 ₫"), ("Tổng phải thu", "1.420.000 ₫"), ("Hạn thanh toán", "25/05/2026"),
            ("Trạng thái", "Chưa thanh toán"), ("Ngày thanh toán", "—"), ("Phương thức", "—"),
        ]),
    ], '<button type="button" class="btn-mgmt-block btn-mgmt-block--blue">Ghi nhận thanh toán (demo)</button>')
    patch_page(
        "quan-ly-thanh-toan.html",
        "Quản lý thanh toán",
        "Quản lý thanh toán",
        "Quản lý thanh toán",
        "<code>UC 5.1</code> — Theo dõi công nợ, thu phí và đối soát VNPay.",
        thead,
        "\n".join(rows),
        drawer,
    )


if __name__ == "__main__":
    patch_sinh_vien()
    patch_phong()
    patch_dang_ky()
    patch_hop_dong()
    patch_thanh_toan()
    subprocess.run([sys.executable, str(ROOT / "build_nojs.py")], check=True)
