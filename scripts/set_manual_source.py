"""Set source=manual on this lab's annotations, preserving a before/after audit."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import getpass
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from cvat_local_setup import LocalCVAT, ROOT


def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if k not in {'id', 'source', 'version'}}
    if isinstance(value, list):
        items = [normalize(v) for v in value]
        return sorted(items, key=lambda v: json.dumps(v, sort_keys=True)) if all(isinstance(v, dict) for v in value) else items
    return value


def change_source(value):
    if isinstance(value, dict):
        if 'source' in value:
            value['source'] = 'manual'
        for v in value.values():
            change_source(v)
    elif isinstance(value, list):
        for v in value:
            change_source(v)


def convert(client, state):
    stamp = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).strftime('%Y%m%d-%H%M%S')
    dest = ROOT / 'work/source-change' / stamp
    dest.mkdir(parents=True, exist_ok=False)
    snapshots = {}
    for group, task in state['tasks'].items():
        task_id = task['id']
        current = client.call('GET', f'tasks/{task_id}')
        if current['project_id'] != state['project_id']:
            raise RuntimeError(f'Task {task_id} không thuộc project Day11')
        before = client.call('GET', f'tasks/{task_id}/annotations')
        (dest / f'{task_id}-before.json').write_text(json.dumps(before, ensure_ascii=False, indent=2))
        snapshots[group] = before
    results = {}
    for group, task in state['tasks'].items():
        task_id = task['id']
        before = snapshots[group]
        payload = {'version': before['version']}
        for kind in ['tags', 'shapes', 'tracks']:
            payload[kind] = deepcopy(before.get(kind, []))
            change_source(payload[kind])
        changed = sum(a != b for kind in ['tags', 'shapes', 'tracks']
                      for a, b in zip(before.get(kind, []), payload[kind]))
        if changed:
            client.call('PATCH', f'tasks/{task_id}/annotations?action=update', json=payload)
        after = client.call('GET', f'tasks/{task_id}/annotations')
        (dest / f'{task_id}-after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2))
        assert normalize(before) == normalize(after), f'{group}: dữ liệu ngoài source thay đổi'
        counts = {}
        for kind in ['tags', 'shapes', 'tracks']:
            assert len(before.get(kind, [])) == len(after.get(kind, []))
            sources = Counter(v.get('source') for v in after.get(kind, []))
            assert set(sources) <= {'manual'}, (group, kind, sources)
            counts[kind] = dict(sources)
        results[group] = {'task_id': task_id, 'changed': changed, 'sources_after': counts,
                          'geometry_and_attributes_unchanged': True}
        print(group, json.dumps(results[group], ensure_ascii=False), flush=True)
    (dest / 'verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print('Audit:', dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--username', default='hocvien')
    args = ap.parse_args()
    state = json.loads((ROOT / 'work/cvat_state.json').read_text())
    client = LocalCVAT(state['base_url'])
    client.call('POST', 'auth/login', json={'username': args.username, 'password': getpass.getpass('CVAT password: ')})
    convert(client, state)


if __name__ == '__main__':
    main()
