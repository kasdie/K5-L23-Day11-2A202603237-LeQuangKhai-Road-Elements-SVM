"""Export two core tasks locally; --final checks completed jobs and creates a manifest."""
import argparse
import getpass
import io
import json
from pathlib import Path
import sys
from urllib.parse import urlparse
import zipfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from road_lab.cvat_xml import parse_bytes
from road_lab.road_check import delivery_manifest, lint


def output_paths(dest, name, final=False):
    if not name.isascii() or not name.isalnum():
        raise ValueError('Tên file dùng chữ/số ASCII, viết liền không dấu')
    paths = [dest / f'{name}-{group}.zip' for group in ['front', 'fisheye']]
    if final:
        paths.append(dest / f'{name}-manifest.json')
    existing = [str(p) for p in paths if p.exists()]
    if existing:
        raise ValueError('File đã tồn tại; lưu bản cũ trước khi export lại: ' + ', '.join(existing))
    return paths


def require_completed(client, state):
    pending = []
    for group in ['front', 'fisheye']:
        task_id = state['tasks'][group]['id']
        jobs = client.items(f'jobs?task_id={task_id}')
        if not jobs or any(job['state'] != 'completed' for job in jobs):
            pending.append(group)
    if pending:
        raise ValueError('Chưa Finish job core: ' + ', '.join(pending) + '. Rà nhãn → Save → Finish the job → Continue, rồi chạy lại.')


def validate_archive(data):
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        if any(Path(n).suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.webp'} for n in zf.namelist()):
            raise ValueError('ZIP có kèm ảnh; cần Save images = OFF')
        names = [n for n in zf.namelist() if n.rsplit('/', 1)[-1] == 'annotations.xml']
        if len(names) != 1:
            raise ValueError('ZIP cần đúng một annotations.xml')
        return parse_bytes(zf.read(names[0]))


def main():
    from cvat_local_setup import LocalCVAT
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--session-file',help='Cookie jar tạm; bỏ qua để nhập mật khẩu trực tiếp')
    ap.add_argument('--username',default='hocvien')
    ap.add_argument('--name',default='hocvien')
    ap.add_argument('--out',type=Path,default=ROOT/'work/exports')
    ap.add_argument('--final',action='store_true',help='Yêu cầu hai job core completed; ghi thêm manifest')
    ap.add_argument('--revision',type=int,default=1)
    args=ap.parse_args()
    if args.revision < 1:
        raise SystemExit('--revision phải từ 1 trở lên')
    try:
        paths = output_paths(args.out, args.name, args.final)
    except ValueError as exc:
        raise SystemExit(str(exc))
    state=json.loads((ROOT/'work/cvat_state.json').read_text())
    client=LocalCVAT(state['base_url'],args.session_file)
    if not args.session_file:
        client.call('POST','auth/login',json={'username':args.username,'password':getpass.getpass('CVAT password: ')})
    if args.final:
        try:
            require_completed(client,state)
        except ValueError as exc:
            raise SystemExit(str(exc))
    args.out.mkdir(parents=True,exist_ok=True)
    images=[]
    for group,path in zip(['front','fisheye'],paths[:2]):
        task_id=state['tasks'][group]['id']
        request=client.call('POST',f'tasks/{task_id}/dataset/export',params={
            'format':'CVAT for images 1.1','save_images':'false','location':'local'})
        result=client.wait(request['rq_id'])
        url=result['result_url']
        if url.startswith('/'):
            url=client.base+url
        if urlparse(url).netloc != urlparse(client.base).netloc:
            raise SystemExit('Export URL không thuộc CVAT local')
        response=client.session.get(url,timeout=90); response.raise_for_status()
        images.extend(validate_archive(response.content))
        path.write_bytes(response.content)
        print(path,len(response.content),'bytes',flush=True)
    findings=lint(images)
    for f in findings:
        print(f'[{f.code} {f.severity}] {f.image}: {f.message}')
    if args.final:
        manifest=delivery_manifest([str(p) for p in paths[:2]],findings,args.name,args.revision)
        paths[2].write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        print('Manifest:',paths[2])
    print(f'{len(images)} ảnh, {len(findings)} cảnh báo; chưa xác nhận chất lượng hình học hay peer-QC.')


if __name__=='__main__':
    main()
