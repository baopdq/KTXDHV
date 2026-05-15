# -*- coding: utf-8 -*-
"""Strip JS, static sidebar, :target modals, no-toast. Run: python build_nojs.py"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

BQL_NAV = [
    ("Chung", None),
    ("tong-quan", "Trang chủ"),
    ("so-do-uc", "Sơ đồ UC"),
    ("doi-mat-khau", "Đổi mật khẩu"),
    ("_sv", "Cổng sinh viên →"),
    ("Quản trị", None),
    ("quan-ly-tai-khoan", "Tài khoản & phân quyền"),
    ("thong-ke-doanh-thu", "Thống kê doanh thu"),
    ("Danh mục & phòng", None),
    ("toa-nha", "Tòa nhà"),
    ("thiet-lap-phong", "Thiết lập phòng KTX"),
    ("tra-cuu-phong", "Tra cứu phòng trống"),
    ("vat-tu-phong", "Vật tư trong phòng"),
    ("Đăng ký & hợp đồng", None),
    ("phe-duyet-don", "Phê duyệt đơn đăng ký"),
    ("thanh-ly-hop-dong", "Thanh lý hợp đồng"),
    ("Cư trú", None),
    ("ho-so-noi-tru", "Hồ sơ nội trú"),
    ("diem-danh", "Điểm danh sinh viên"),
    ("Thông báo", None),
    ("quan-ly-thong-bao", "Quản lý thông báo"),
    ("Báo cáo", None),
    ("thong-ke-lap-day", "Thống kê lấp đầy"),
    ("Tích hợp", None),
    ("tich-hop", "VNPay & tác vụ hệ thống"),
]

SV_NAV = [
    ("Menu", None),
    ("trang-chu", "Trang chủ"),
    ("tra-cuu-phong", "Tra cứu phòng trống"),
    ("dang-ky-phong", "Đăng ký thuê phòng"),
    ("minh-chung-uu-tien", "Minh chứng ưu tiên"),
    ("bao-cao-hu-hong", "Báo cáo hư hỏng"),
    ("hoa-don-thanh-toan", "Hóa đơn & thanh toán"),
    ("don-cua-toi", "Đơn của tôi"),
    ("doi-mat-khau", "Đổi mật khẩu"),
    ("thong-bao", "Thông báo"),
]

CSS_NOJS = """
/* --- Không JS: modal :target, mobile, ẩn vùng toast --- */
.modal-backdrop { display: none; }
.modal-backdrop:target { display: flex; }
.modal { position: relative; }
.modal-close {
  position: absolute;
  top: 10px;
  right: 14px;
  font-size: 1.4rem;
  line-height: 1;
  text-decoration: none;
  color: var(--muted);
}
.toast-area { display: none !important; }
@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { display: flex !important; position: relative; width: 100%; max-width: none; }
  .menu-toggle { display: none !important; }
}
"""


def bql_sidebar(active: str) -> str:
    parts = [
        '<div class="sidebar-brand sidebar-brand--logo"><img class="sidebar-brand__logo" src="assets/logo-dai-hoc-vinh.jpg" alt="Logo Đại học Vinh" width="48" height="48" /><div><strong>Trường Đại học Vinh</strong><span>KTX · Ban quản lý</span></div></div>'
    ]
    for item in BQL_NAV:
        if item[1] is None:
            parts.append(f'<div class="nav-section">{item[0]}</div>')
            continue
        slug, label = item
        if slug == "_sv":
            parts.append(f'<a href="sinhvien/trang-chu.html" class="nav-link">{label}</a>')
            continue
        href = f"{slug}.html"
        act = " is-active" if slug == active else ""
        parts.append(f'<a href="{href}" class="nav-link{act}">{label}</a>')
    return "\n      ".join(parts)


def sv_sidebar(active: str) -> str:
    parts = [
        '<div class="sidebar-brand sidebar-brand--sv"><img class="sidebar-brand__logo" src="../assets/logo-dai-hoc-vinh.jpg" alt="Logo Đại học Vinh" width="48" height="48" /><div><strong>Cổng sinh viên KTX</strong><span>Đại học Vinh</span></div></div>'
    ]
    for item in SV_NAV:
        if item[1] is None:
            parts.append(f'<div class="nav-section">{item[0]}</div>')
            continue
        slug, label = item
        href = f"{slug}.html"
        act = " is-active" if slug == active else ""
        parts.append(f'<a href="{href}" class="nav-link{act}">{label}</a>')
    return "\n      ".join(parts)


def strip_scripts(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", html, flags=re.I)
    html = re.sub(r"<script\b[^>]*/>", "", html, flags=re.I)
    return html


def inject_css(html: str) -> str:
    if "/* --- Không JS:" in html:
        return html
    return html.replace("</style>", CSS_NOJS + "\n</style>", 1)


def inject_student_css(html: str, depth: int = 1) -> str:
    if "ktx-student.css" in html:
        return html
    prefix = "../" * depth if depth else ""
    link = f'    <link rel="stylesheet" href="{prefix}css/ktx-student.css" />\n'
    needle = f'    <link rel="stylesheet" href="{prefix}css/ktx-ui.css" />'
    if needle in html:
        return html.replace(needle, needle + "\n" + link, 1)
    return html


def inject_print_css(html: str, depth: int = 0) -> str:
    """Thêm ktx-print.css nếu chưa có."""
    if "ktx-print.css" in html:
        return html
    prefix = "../" * depth if depth else ""
    link = f'    <link rel="stylesheet" href="{prefix}css/ktx-print.css" />\n'
    needle = f'    <link rel="stylesheet" href="{prefix}css/ktx-ui.css" />'
    if needle in html:
        return html.replace(needle, needle + "\n" + link, 1)
    return html


def wire_print_buttons(html: str) -> str:
    html = html.replace(
        '<button type="button" class="btn-mgmt-outline">In danh sách (demo)</button>',
        '<button type="button" class="btn-mgmt-outline" onclick="window.print()">In danh sách</button>',
    )
    return html


def topbar_bql():
    return """<header class="topbar">
          <div class="topbar-left">
            <span class="role-badge">BQL (demo tĩnh)</span>
          </div>
          <div class="topbar-actions">
            <a href="doi-mat-khau.html" class="btn btn-ghost btn-sm">Đổi mật khẩu</a>
            <a href="dang-nhap.html" class="btn btn-secondary btn-sm">Trang đăng nhập</a>
          </div>
        </header>"""


def topbar_sv():
    return """<header class="topbar">
          <div class="topbar-left">
            <div class="student-topbar-brand">
              <img src="../assets/logo-dai-hoc-vinh.jpg" alt="" width="32" height="32" />
              <div>
                <strong>Đại học Vinh</strong>
                <small>KTX · Cổng sinh viên</small>
              </div>
            </div>
            <span class="role-badge">Sinh viên</span>
          </div>
          <div class="topbar-actions">
            <a href="doi-mat-khau.html" class="btn btn-ghost btn-sm">Đổi mật khẩu</a>
            <a href="dang-nhap.html" class="btn btn-secondary btn-sm">Đăng nhập SV</a>
          </div>
        </header>"""


def replace_topbar(html: str, kind: str):
    nb = topbar_bql() if kind == "bql" else topbar_sv()
    return re.sub(r"<header class=\"topbar\">[\s\S]*?</header>", nb, html, count=1)


def replace_aside(html: str, inner: str):
    return re.sub(
        r'<aside id="sidebar" class="sidebar">\s*</aside>',
        f'<aside id="sidebar" class="sidebar">\n      {inner}\n      </aside>',
        html,
        count=1,
    )


def fix_quan_ly(html: str) -> str:
    html = html.replace(
        '<button type="button" class="btn btn-primary" data-open-modal="modal-add-user">Thêm tài khoản</button>',
        '<a href="#modal-add-user" class="btn btn-primary">Thêm tài khoản</a>',
    )
    html = html.replace(
        '<button type="button" class="btn btn-ghost btn-sm" data-open-modal="modal-roles">Phân quyền</button>',
        '<a href="#modal-roles" class="btn btn-ghost btn-sm">Phân quyền</a>',
    )
    html = html.replace(
        '<button type="button" class="btn btn-danger btn-sm" data-open-modal="modal-lock">Khóa</button>',
        '<a href="#modal-lock" class="btn btn-danger btn-sm">Khóa</a>',
    )
    html = html.replace(
        '<div id="modal-add-user" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal">',
        '<div id="modal-add-user" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal"><a href="#" class="modal-close" aria-label="Đóng">×</a>',
    )
    html = html.replace(
        '<div id="modal-lock" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal">',
        '<div id="modal-lock" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal"><a href="#" class="modal-close" aria-label="Đóng">×</a>',
    )
    html = html.replace(
        '<div id="modal-roles" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal">',
        '<div id="modal-roles" class="modal-backdrop" role="dialog" aria-modal="true">\n      <div class="modal"><a href="#" class="modal-close" aria-label="Đóng">×</a>',
    )
    html = html.replace(
        '<button type="button" class="btn btn-secondary" data-close-modal>Hủy</button>',
        '<a href="#" class="btn btn-secondary">Hủy</a>',
    )
    html = html.replace(
        '<button type="submit" class="btn btn-primary">Lưu</button>',
        '<a href="#" class="btn btn-primary">Lưu (demo)</a>',
        1,
    )
    html = html.replace(
        '<button type="submit" class="btn btn-danger">Xác nhận khóa</button>',
        '<a href="#" class="btn btn-danger">Xác nhận khóa (demo)</a>',
    )
    html = html.replace(
        '<button type="submit" class="btn btn-primary">Lưu phân quyền</button>',
        '<a href="#" class="btn btn-primary">Lưu phân quyền (demo)</a>',
    )
    html = html.replace('<form id="form-add-user">', '<div>')
    html = html.replace('<form id="form-lock-confirm">', '<div>')
    html = html.replace('<form id="form-roles-save">', '<div>')
    for _ in range(3):
        html = html.replace("</form>", "</div>", 1)
    return html


def fix_demo_toast_buttons(html: str) -> str:
    """Chỉ thay button có data-demo-toast -> link (tránh replace </button> toàn cục)."""

    def repl(m):
        cls = m.group(1)
        text = m.group(2)
        return f'<a href="#" class="{cls}">{text} (demo)</a>'

    return re.sub(
        r'<button type="button"\s+class="([^"]+)"\s+data-demo-toast="[^"]*">([^<]+)</button>',
        repl,
        html,
    )


def fix_forms_demo(html: str) -> str:
    """form[data-demo]: đổi submit thành link để không cần JS"""
    html = html.replace('type="submit"', 'type="button"')
    return html


def process_bql(path: Path):
    stem = path.stem
    html = path.read_text(encoding="utf-8")
    html = strip_scripts(html)
    html = inject_css(html)
    html = inject_print_css(html, 0)
    html = wire_print_buttons(html)
    html = replace_aside(html, bql_sidebar(stem))
    html = replace_topbar(html, "bql")
    html = re.sub(r'<div id="toast-area"[^>]*></div>\s*', "", html)
    html = re.sub(r"\s*data-bql-page=\"[^\"]*\"", "", html)
    html = re.sub(r"\s*data-bql-admin-only=\"[^\"]*\"", "", html)
    html = fix_demo_toast_buttons(html)
    if stem == "quan-ly-tai-khoan":
        html = fix_quan_ly(html)
    path.write_text(html, encoding="utf-8")


def ensure_student_sidebar_visible(html: str) -> str:
    """`.sidebar{display:none}` trong @media (mobile) che menu; SV không JS cần sidebar luôn hiện."""
    old = """.student-app .sidebar {
  background: linear-gradient(180deg, #065f46 0%, #047857 100%);
}"""
    new = """.student-app .sidebar {
  display: flex !important;
  background: var(--primary);
}"""
    if old in html:
        return html.replace(old, new, 1)
    return html


def fix_sv_mobile_sidebar_scope(html: str) -> str:
    """@media mobile ẩn mọi .sidebar — trên cổng SV (có .student-app) làm mất menu."""
    old = """  .sidebar {
    display: none;
  }

  .sidebar.is-open {
    display: flex;
    position: fixed;
    inset: 0;
    z-index: 100;
    max-width: 280px;
    box-shadow: 8px 0 24px rgba(0, 0, 0, 0.15);
  }"""
    new = """  /* Chỉ ẩn sidebar mobile cho BQL (có JS menu); cổng SV luôn có .student-app */
  .app:not(.student-app) .sidebar {
    display: none;
  }

  .app:not(.student-app) .sidebar.is-open {
    display: flex;
    position: fixed;
    inset: 0;
    z-index: 100;
    max-width: 280px;
    box-shadow: 8px 0 24px rgba(0, 0, 0, 0.15);
  }"""
    if old in html:
        return html.replace(old, new, 1)
    return html


def process_sv(path: Path):
    stem = path.stem
    html = path.read_text(encoding="utf-8")
    html = strip_scripts(html)
    html = inject_css(html)
    html = inject_print_css(html, 1)
    html = inject_student_css(html, 1)
    html = fix_sv_mobile_sidebar_scope(html)
    html = ensure_student_sidebar_visible(html)
    html = replace_aside(html, sv_sidebar(stem))
    html = replace_topbar(html, "sv")
    html = re.sub(r'<div id="toast-area"[^>]*></div>\s*', "", html)
    html = re.sub(r"\s*data-sv-page=\"[^\"]*\"", "", html)
    html = fix_demo_toast_buttons(html)
    path.write_text(html, encoding="utf-8")


def main():
    for p in sorted(ROOT.glob("*.html")):
        if p.name == "index.html":
            t = inject_css(strip_scripts(p.read_text(encoding="utf-8")))
            p.write_text(t, encoding="utf-8")
            continue
        if p.name == "dang-nhap.html":
            t = strip_scripts(p.read_text(encoding="utf-8"))
            t = inject_css(t)
            t = re.sub(
                r"<form id=\"login-form\">[\s\S]*?</form>",
                '<p class="hint">Bản <strong>không dùng JavaScript</strong>. Chọn:</p>'
                '<ul style="text-align:left;margin:16px 0;padding-left:1.2rem">'
                '<li><a class="btn btn-primary" style="display:inline-block;margin:6px 0" href="tong-quan.html">Trang chủ BQL</a></li>'
                '<li><a class="btn btn-primary" style="display:inline-block;margin:6px 0" href="sinhvien/trang-chu.html">Cổng sinh viên</a></li>'
                "</ul>",
                t,
                count=1,
            )
            p.write_text(t, encoding="utf-8")
            continue
        process_bql(p)

    sv = ROOT / "sinhvien"
    for p in sorted(sv.glob("*.html")):
        if p.name == "index.html":
            t = strip_scripts(p.read_text(encoding="utf-8"))
            p.write_text(t, encoding="utf-8")
            continue
        if p.name == "dang-nhap.html":
            t = strip_scripts(p.read_text(encoding="utf-8"))
            t = inject_css(t)
            t = re.sub(
                r"<form id=\"student-login-form\">[\s\S]*?</form>",
                '<p class="hint">Không dùng JS — vào trực tiếp:</p>'
                '<p><a class="btn btn-primary" href="trang-chu.html">Trang chủ sinh viên</a></p>',
                t,
                count=1,
            )
            p.write_text(t, encoding="utf-8")
            continue
        process_sv(p)

    print("OK")


if __name__ == "__main__":
    main()
