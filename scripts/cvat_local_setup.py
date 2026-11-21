"""Create the Day 11 project and upload the class pack to local CVAT only."""
from __future__ import annotations

import argparse
import getpass
import http.cookiejar
import json
from contextlib import ExitStack
from pathlib import Path
import sys
import time
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from road_lab.taxonomy import CORE_IMAGES, EXTRA_IMAGES, expected_camera, image_slot, raw_labels


class LocalCVAT:
    def __init__(self, base="http://localhost:8080", session_file=None):
        if urlparse(base).hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Công cụ này chỉ kết nối CVAT local")
        self.base = base.rstrip("/")
        self.session = requests.Session()
        if session_file:
            jar = http.cookiejar.MozillaCookieJar(session_file)
            jar.load(ignore_discard=True)
            self.session.cookies.update(jar)

    def call(self, method, path, **kwargs):
        csrf = next((c.value for c in self.session.cookies if c.name == "csrftoken"), None)
        headers = {"Referer": self.base + "/"}
        if csrf:
            headers["X-CSRFToken"] = csrf
        response = self.session.request(method, self.base + "/api/" + path,
                                        headers=headers, timeout=90, **kwargs)
        if not response.ok:
            raise RuntimeError(f"CVAT {method} {path}: HTTP {response.status_code}: {response.text[:500]}")
        return response.json() if response.content else None

    def items(self, path):
        result = self.call("GET", path + ("&" if "?" in path else "?") + "page_size=100")
        items = result["results"]
        while result.get("next"):
            result = self.call("GET", result["next"].split("/api/", 1)[1])
            items.extend(result["results"])
        return items

    def wait(self, request_id):
        for _ in range(120):
            state = self.call("GET", f"requests/{request_id}")
            if state["status"] == "finished":
                return state
            if state["status"] == "failed":
                raise RuntimeError(f"CVAT request failed: {state.get('message')}")
            time.sleep(1)
        raise RuntimeError(f"CVAT chưa xong; kiểm Requests: {request_id}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://localhost:8080")
    parser.add_argument("--username", default="hocvien")
    parser.add_argument("--name", default="hocvien", help="Tên dùng trong d11-road-<tên>")
    parser.add_argument("--session-file", help="Cookie jar tạm; không đưa vào Git")
    args = parser.parse_args()
    files = sorted(p for p in (ROOT / "data").iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    slots = [image_slot(p.name) for p in files]
    if len(slots) != 28 or set(slots) != CORE_IMAGES | EXTRA_IMAGES:
        raise SystemExit("Cần đúng 28 ảnh A01–A16, B01–B12, mỗi slot một ảnh trong data/")
    if any(expected_camera(p.name) is None for p in files):
        raise SystemExit("Tên ảnh không xác định được camera; giữ tên gói ảnh của lớp")
    client = LocalCVAT(args.base, args.session_file)
    if not args.session_file:
        client.call("POST", "auth/login", json={"username": args.username, "password": getpass.getpass("CVAT password: ")})
    project_name = f"d11-road-{args.name}"
    project = next((p for p in client.items("projects") if p["name"] == project_name), None)
    if project is None:
        project = client.call("POST", "projects", json={"name": project_name, "labels": raw_labels()})
    labels = client.items(f"labels?project_id={project['id']}")
    def signature(label):
        return (label['name'], label['type'], sorted(
            (a['name'], a['input_type'], tuple(a['values']), a['default_value'], a['mutable'])
            for a in label['attributes']))
    if sorted(map(signature, labels)) != sorted(map(signature, raw_labels())):
        raise SystemExit("Labels của project đã có không khớp Road v1.0; không sửa đè")
    state = {"base_url": client.base, "project_id": project["id"], "project_name": project_name,
             "project_url": f"{client.base}/projects/{project['id']}", "tasks": {}}
    for name, prefix, low, high in [("front", "A", 1, 12), ("front-extra", "A", 13, 16),
                                    ("fisheye", "B", 1, 8), ("fisheye-extra", "B", 9, 12)]:
        selected = [p for p in files if p.name.startswith(prefix) and low <= int(image_slot(p.name)[1:]) <= high]
        task = next((t for t in client.items(f"tasks?project_id={project['id']}") if t['name'] == name), None)
        if task is None:
            task = client.call("POST", "tasks", json={"name": name, "project_id": project['id']})
        task = client.call("GET", f"tasks/{task['id']}")
        if task.get('data') is None:
            with ExitStack() as stack:
                uploads = [(f"client_files[{i}]", (p.name, stack.enter_context(p.open('rb')))) for i, p in enumerate(selected)]
                request = client.call("POST", f"tasks/{task['id']}/data", data={"image_quality": 100, "sorting_method": "lexicographical"}, files=uploads)
            client.wait(request['rq_id'])
        frames = client.call("GET", f"tasks/{task['id']}/data/meta")['frames']
        if sorted(f['name'] for f in frames) != sorted(p.name for p in selected):
            raise SystemExit(f"Ảnh task {name} không khớp gói local; không ghi đè")
        jobs = client.items(f"jobs?task_id={task['id']}")
        state['tasks'][name] = {"id": task['id'], "images": len(frames), "jobs": [j['id'] for j in jobs]}
        print(name, state['tasks'][name], flush=True)
        (ROOT / 'work').mkdir(exist_ok=True)
        (ROOT / 'work/cvat_state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(state['project_url'])


if __name__ == "__main__":
    main()
