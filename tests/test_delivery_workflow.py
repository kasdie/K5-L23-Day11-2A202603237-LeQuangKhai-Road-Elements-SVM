"""Delivery regressions: stale manifests, accidental image uploads, and overwrites."""
import json
from pathlib import Path
import sys
import zipfile

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_delivery import check_bundle
from export_local_draft import output_paths, require_completed, validate_archive
from road_lab.cvat_xml import load, write
from road_lab.road_check import delivery_manifest, lint
from road_lab.synthetic import synthetic_gt


@pytest.fixture
def bundle(tmp_path):
    images = synthetic_gt()
    paths = [tmp_path / 'an-front.zip', tmp_path / 'an-fisheye.zip']
    write([im for im in images if im.name.startswith('A')], paths[0])
    write([im for im in images if im.name.startswith('B')], paths[1])
    findings = lint(load(paths[0]) + load(paths[1]))
    manifest = delivery_manifest([str(p) for p in paths], findings, 'an', 1)
    (tmp_path / 'an-manifest.json').write_text(json.dumps(manifest))
    (tmp_path / 'an-report.md').write_text('Báo cáo cá nhân đã điền (fixture tổng hợp).')
    (tmp_path / 'an-qc1-for-binh.md').write_text('Phiếu đã điền (fixture tổng hợp).')
    return tmp_path


def test_matching_bundle_is_not_a_quality_approval(bundle):
    result = check_bundle(bundle, 'an', 'binh')
    assert result['issues'] == []
    assert result['images'] == 20
    assert result['quality_approved'] is False


def test_modified_zip_invalidates_manifest(bundle):
    path = bundle / 'an-front.zip'
    images = load(path)
    images[0].shapes[0].points[0] = (400.0, 710.0)
    write(images, path)
    result = check_bundle(bundle, 'an', 'binh')
    assert any('files' in issue and 'Manifest' in issue for issue in result['issues'])


def test_embedded_image_rejected_on_download_and_delivery(bundle):
    path = bundle / 'an-front.zip'
    with zipfile.ZipFile(path, 'a') as zf:
        zf.writestr('images/A01.jpg', b'not-a-real-photo')
    with pytest.raises(ValueError, match='kèm ảnh'):
        validate_archive(path.read_bytes())
    assert any('kèm ảnh' in issue for issue in check_bundle(bundle, 'an', 'binh')['issues'])


def test_unfinished_jobs_prevent_final_export():
    class Client:
        def items(self, path):
            return [{'state': 'new' if '40' in path else 'completed'}]
    state = {'tasks': {'front': {'id': 40}, 'fisheye': {'id': 42}}}
    with pytest.raises(ValueError, match='front'):
        require_completed(Client(), state)


def test_existing_second_zip_prevents_any_new_export(tmp_path):
    (tmp_path / 'an-fisheye.zip').write_bytes(b'keep this revision')
    with pytest.raises(ValueError, match='đã tồn tại'):
        output_paths(tmp_path, 'an', final=True)
    assert not (tmp_path / 'an-front.zip').exists()


def test_pending_peer_qc_is_flagged(bundle):
    (bundle / 'an-qc1-for-binh.md').write_text('CHƯA KIỂM — số lỗi: __')
    assert any('qc1' in issue for issue in check_bundle(bundle, 'an', 'binh')['issues'])
