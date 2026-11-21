"""The public report must never embed classroom image pixels."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from prepare_lms_repo import public_report, prepare, FILES
import hashlib
import json
import zipfile


def test_public_report_removes_embedded_and_linked_images():
    result = public_report('# Report\n![front](data:image/jpeg;base64,ABC123)\n![fisheye](local.png)')
    assert 'data:image' not in result
    assert '![' not in result
    assert '**front:**' in result and '**fisheye:**' in result


def test_public_report_refuses_html_image_tags():
    with pytest.raises(ValueError, match='ảnh nhúng'):
        public_report('<img src="data:image/jpeg;base64,ABC123">')


@pytest.fixture
def source_bundle(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    entries = []
    for name in FILES[:2]:
        path = source / name
        with zipfile.ZipFile(path, 'w') as zf:
            zf.writestr('annotations.xml', '<annotations><version>1.1</version></annotations>')
        entries.append({'file': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (source / FILES[2]).write_text(json.dumps({'files': entries}))
    for name in FILES[3:]:
        (source / name).write_text('# Draft\n![Evidence](data:image/jpeg;base64,ABC123)')
    return source


def test_prepared_bundle_strips_images_from_report_and_peer_qc(source_bundle, tmp_path):
    dest = tmp_path / 'public'
    prepare(source_bundle, dest)
    assert sorted(p.name for p in dest.iterdir()) == sorted(FILES)
    for name in FILES[3:]:
        assert 'data:image' not in (dest / name).read_text()
    for name in FILES[:3]:
        assert (dest / name).read_bytes() == (source_bundle / name).read_bytes()


def test_missing_zip_checksum_is_rejected_before_writing(source_bundle, tmp_path):
    manifest = source_bundle / FILES[2]
    data = json.loads(manifest.read_text())
    data['files'].pop()
    manifest.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='đúng hai ZIP'):
        prepare(source_bundle, tmp_path / 'public')
    assert not (tmp_path / 'public').exists()


def test_extra_archive_member_is_rejected(source_bundle, tmp_path):
    path = source_bundle / FILES[0]
    with zipfile.ZipFile(path, 'a') as zf:
        zf.writestr('images/classroom.png', b'pixel bytes')
    manifest = source_bundle / FILES[2]
    data = json.loads(manifest.read_text())
    data['files'][0]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='không kèm ảnh'):
        prepare(source_bundle, tmp_path / 'public')


def test_existing_destination_is_preserved(source_bundle, tmp_path):
    dest = tmp_path / 'public'
    dest.mkdir()
    sentinel = dest / FILES[1]
    sentinel.write_bytes(b'previous reviewed revision')
    with pytest.raises(ValueError, match='không ghi đè'):
        prepare(source_bundle, dest)
    assert sentinel.read_bytes() == b'previous reviewed revision'
    assert len(list(dest.iterdir())) == 1
