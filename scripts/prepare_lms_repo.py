"""Prepare the five LMS files for GitHub without copying dataset screenshots."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ['lequangkhai-front.zip', 'lequangkhai-fisheye.zip', 'lequangkhai-manifest.json',
         'lequangkhai-qc1-for-hoangkimchi.md', 'lequangkhai-report.md']


def without_images(text):
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)',
                  lambda m: f'**{m[1]}:** ảnh minh chứng lưu riêng; cung cấp qua kênh riêng của lớp.', text)
    if re.search(r'data:image|<img\b|!\[', text, re.I):
        raise ValueError('Báo cáo còn ảnh nhúng; kiểm lại trước khi tạo bản GitHub')
    return text


def public_report(text):
    text = without_images(text)
    text = text.replace(
        'Ảnh dưới đây được chụp lại từ CVAT local trong phiên cập nhật báo cáo, không dùng ảnh minh họa tổng hợp. Ảnh được nhúng trực tiếp để không phụ thuộc thư mục ảnh ngoài; bản HTML xem kèm cũng chứa các ảnh này.',
        'Các ảnh minh chứng được chụp từ CVAT local và lưu trong bản báo cáo đầy đủ trên máy. Bản GitHub này chỉ giữ mô tả; không nhúng pixel dataset. Cần gửi minh chứng qua kênh riêng được lớp cho phép để coach kiểm mục ảnh chụp.')
    text = text.replace('## 6. Ảnh chụp màn hình', '## 6. Ảnh chụp màn hình — minh chứng lưu riêng')
    return ('> BẢN GITHUB: ảnh minh chứng được lưu riêng; trạng thái QC và giới hạn kiểm tra '
            'được ghi trong báo cáo và phiếu QC đi kèm.\n\n' + text)


def prepare(source, destination):
    data = {name: (source / name).read_bytes() for name in FILES}
    manifest = json.loads(data['lequangkhai-manifest.json'])
    if sorted(entry['file'] for entry in manifest['files']) != sorted(FILES[:2]):
        raise ValueError('Manifest phải mô tả đúng hai ZIP của bộ nộp')
    for entry in manifest['files']:
        if entry['file'] not in FILES[:2]:
            raise ValueError('Manifest có tên ZIP không thuộc bộ nộp')
        if hashlib.sha256(data[entry['file']]).hexdigest() != entry['sha256']:
            raise ValueError('Manifest không khớp ZIP; chạy lint --manifest lại trước')
    for name in FILES[:2]:
        with zipfile.ZipFile(source / name) as zf:
            if len(zf.namelist()) != 1 or zf.namelist()[0] != 'annotations.xml':
                raise ValueError(f'{name}: chỉ nhận ZIP chứa annotations.xml, không kèm ảnh/tệp khác')
    data['lequangkhai-report.md'] = public_report(data['lequangkhai-report.md'].decode('utf-8')).encode('utf-8')
    data['lequangkhai-qc1-for-hoangkimchi.md'] = without_images(data['lequangkhai-qc1-for-hoangkimchi.md'].decode('utf-8')).encode('utf-8')
    if any((destination / name).exists() for name in FILES):
        raise ValueError('Thư mục đích đã có bộ file; dùng --out mới để không ghi đè')
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in data.items():
        (destination / name).write_bytes(content)
    print(f'Prepared {len(data)} files at {destination}; no publication performed.')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, default=ROOT / 'submissions')
    ap.add_argument('--out', type=Path, default=ROOT / 'lms_submission')
    args = ap.parse_args()
    prepare(args.source, args.out)


if __name__ == '__main__':
    main()
