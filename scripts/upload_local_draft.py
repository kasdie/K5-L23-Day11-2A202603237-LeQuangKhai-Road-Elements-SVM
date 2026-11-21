"""Upload inspected draft geometry into EMPTY Day11 local tasks; never overwrite work."""
import argparse
import json
from pathlib import Path
from cvat_local_setup import LocalCVAT, ROOT
from road_lab.taxonomy import SHAPE_LABELS, image_slot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session-file', required=True)
    args = parser.parse_args()
    state = json.loads((ROOT/'work/cvat_state.json').read_text())
    draft = json.loads((ROOT/'work/draft_annotations.json').read_text())
    client = LocalCVAT(state['base_url'], args.session_file)
    labels = {l['name']: l for l in client.items(f"labels?project_id={state['project_id']}")}
    def attrs(label, values):
        specs = {a['name']: a for a in labels[label]['attributes']}
        if set(values) != set(specs):
            raise ValueError(f'{label}: thiếu/thừa thuộc tính')
        for name, value in values.items():
            allowed = ['true','false'] if specs[name]['input_type'] == 'checkbox' else specs[name]['values']
            if value not in allowed:
                raise ValueError(f'{label}.{name}: giá trị không hợp lệ {value}')
        return [{'spec_id': specs[k]['id'], 'value': v} for k,v in values.items()]
    for name, task in state['tasks'].items():
        task_id = task['id']
        before = client.call('GET', f'tasks/{task_id}/annotations')
        backup = ROOT/f'work/task-{task_id}-before-draft.json'
        if not backup.exists():
            backup.write_text(json.dumps(before,ensure_ascii=False,indent=2))
        if before['shapes'] or before['tags'] or before['tracks']:
            print(f'SKIP {name}: task đã có nhãn, không ghi đè',flush=True)
            continue
        frames = client.call('GET', f'tasks/{task_id}/data/meta')['frames']
        payload = {'version':before['version'],'tags':[],'shapes':[],'tracks':[]}
        for frame, meta in enumerate(frames):
            im = draft[image_slot(meta['name'])]
            assert (im['name'],im['width'],im['height']) == (meta['name'],meta['width'],meta['height'])
            for label, value in im['tags'].items():
                payload['tags'].append({'frame':frame,'label_id':labels[label]['id'],
                                        'attributes':attrs(label,{'value':value}),'source':'auto'})
            for s in im['shapes']:
                assert all(0<=x<=im['width'] and 0<=y<=im['height'] for x,y in s['points'])
                payload['shapes'].append({'frame':frame,'label_id':labels[s['label']]['id'],
                    'type':SHAPE_LABELS[s['label']]['type'],'points':[v for p in s['points'] for v in p],
                    'attributes':attrs(s['label'],s['attributes']),'occluded':s['occluded'],'source':'auto'})
        client.call('PATCH',f'tasks/{task_id}/annotations?action=create',json=payload)
        after = client.call('GET', f'tasks/{task_id}/annotations')
        assert len(after['tags'])==len(payload['tags']) and len(after['shapes'])==len(payload['shapes'])
        (ROOT/f'work/task-{task_id}-draft.json').write_text(json.dumps(after,ensure_ascii=False,indent=2))
        print(name, 'tags',len(after['tags']),'shapes',len(after['shapes']),flush=True)


if __name__ == '__main__':
    main()
