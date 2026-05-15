# -*- coding: utf-8 -*-
"""Thêm thanh CRUD+I (Thêm/Sửa/Xóa/Xuất/Nhập) vào các trang quản lý. Chạy: python patch_mgmt_crud_toolbar.py"""
from __future__ import annotations

import re
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

PAGES = [
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


def make_toolbar(add_href: str, add_label: str) -> str:
    return f"""              <div class="mgmt-head__actions mgmt-crud-toolbar" role="toolbar" aria-label="Thêm sửa xóa nhập xuất">
                <a href="{add_href}" class="btn-mgmt-primary mgmt-crud-toolbar__primary">{add_label}</a>
                <a href="#modal-mgmt-batch-edit" class="btn-mgmt-outline">Sửa</a>
                <a href="#modal-mgmt-batch-delete" class="btn-mgmt-outline mgmt-crud-toolbar__danger">Xóa</a>
                <button type="button" class="btn-mgmt-outline">Xuất</button>
                <label class="btn-mgmt-outline mgmt-crud-toolbar__import">
                  Nhập
                  <input type="file" accept=".csv,.xlsx,.xls" aria-label="Nhập từ file (demo)" />
                </label>
              </div>"""


def inject_modals(html: str) -> str:
    if 'id="modal-mgmt-batch-edit"' in html:
        return html
    if "</body>" not in html:
        return html
    return html.replace("</body>", MODALS + "\n</body>", 1)


def patch_file(rel: str, href: str, label: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    repl = make_toolbar(href, label)
    text2, n = HEADER_ACTIONS_RE.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit(f"{rel}: không tìm thấy mgmt-head__actions (thay được {n} lần)")
    path.write_text(inject_modals(text2), encoding="utf-8")


def main() -> None:
    for rel, h, lab in PAGES:
        patch_file(rel, h, lab)
        print("OK", rel)


if __name__ == "__main__":
    main()
