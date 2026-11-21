"""Check the five local delivery files; this does not grade annotation quality."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from road_lab.cvat_xml import CvatFormatError, load
from road_lab.road_check import delivery_manifest, lint
from road_lab.taxonomy import CORE_FRONT, CORE_FISHEYE, EXTRA_FRONT, EXTRA_FISHEYE, image_slot


def check_bundle(directory: Path, name: str, peer: str) -> dict:
    for value in (name, peer):
        if not value.isascii() or not value.isalnum():
            raise ValueError('Tên người nộp/bạn QC cần viết liền không dấu, dùng chữ/số ASCII')
    names = [f'{name}-front.zip', f'{name}-fisheye.zip', f'{name}-manifest.json',
             f'{name}-qc1-for-{peer}.md', f'{name}-report.md']
    issues = [f'Thiếu {n}' for n in names if not (directory / n).is_file()]
    images = []
    paths = [directory / n for n in names[:2]]
    for path, core, extra in zip(paths, [CORE_FRONT, CORE_FISHEYE], [EXTRA_FRONT, EXTRA_FISHEYE]):
        if not path.is_file():
            continue
        try:
            with zipfile.ZipFile(path) as zf:
                if any(Path(n).suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.webp'} for n in zf.namelist()):
                    issues.append(f'{path.name}: ZIP có kèm ảnh')
                if sum(n.rsplit('/', 1)[-1] == 'annotations.xml' for n in zf.namelist()) != 1:
                    raise ValueError('cần đúng một annotations.xml')
            batch = load(path)
        except (OSError, CvatFormatError, ValueError, zipfile.BadZipFile) as exc:
            issues.append(f'{path.name}: không đọc được ({exc})')
            continue
        slots = [image_slot(im.name) for im in batch]
        missing = sorted(set(core) - set(slots))
        if missing:
            issues.append(f'{path.name}: còn thiếu ảnh core để hoàn thành đủ lô: {", ".join(missing)}')
        if any(s not in set(core + extra) for s in slots):
            issues.append(f'{path.name}: có ảnh sai nhóm/ngoài lô')
        if len(slots) != len(set(slots)):
            issues.append(f'{path.name}: slot bị trùng')
        for im in batch:
            if not im.shapes:
                issues.append(f'{im.name}: mới có tag hoặc chưa có hình; cần rà xem có đối tượng phải gán không')
        images.extend(batch)
    findings = lint(images)
    manifest_path = directory / names[2]
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            if not isinstance(manifest, dict):
                raise ValueError('cấu trúc manifest phải là object')
            revision = manifest.get('revision')
            if type(revision) is not int or revision < 1:
                issues.append('Manifest: revision phải là số nguyên >= 1')
            if all(p.is_file() for p in paths) and len(images) > 0:
                fresh = delivery_manifest([str(p) for p in paths], findings, name, 1)
                for key in ('manifest', 'format', 'guideline', 'name', 'files', 'lint'):
                    if manifest.get(key) != fresh[key]:
                        issues.append(f'Manifest không khớp ZIP/tên hiện tại: {key}; chạy lint --manifest lại')
        except (OSError, ValueError, TypeError) as exc:
            issues.append(f'Manifest không đọc được: {exc}')
    for filename in names[3:]:
        path = directory / filename
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        if not text.strip() or re.search(r'CHƯA[ _](?:XÁC NHẬN|GHÉP|GHEP|KIỂM|CÓ)|NHÁP KIỂM THỬ|TODO|__', text):
            issues.append(f'{filename}: còn chỗ trống/dấu chờ trong mẫu; cần hoàn thiện thủ công')
    return {'issues': issues, 'lint_findings': [f.__dict__ for f in findings],
            'images': len(images), 'shapes': sum(len(im.shapes) for im in images),
            'required_files': names, 'quality_approved': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=Path, default=ROOT / 'submissions')
    ap.add_argument('--name', required=True)
    ap.add_argument('--peer', required=True)
    args = ap.parse_args()
    try:
        result = check_bundle(args.directory, args.name, args.peer)
    except ValueError as exc:
        ap.error(str(exc))
    for issue in result['issues']:
        print('CẦN BỔ SUNG:', issue)
    for f in result['lint_findings']:
        print(f"[{f['code']} {f['severity']}] {f['image']}: {f['message']}")
    print(f"Đọc được {result['images']} ảnh, {result['shapes']} hình. Đây là kiểm file, không phải điểm/Release.")
    if any(f['code'] == 'QC1-02' for f in result['lint_findings']):
        print('QC1-02 chỉ được miễn khi coach đã xác nhận không thấy vạch và bạn ghi vào phiếu. Công cụ giữ nguyên cảnh báo.')
    return 1 if result['issues'] else 2 if result['lint_findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
