"""Capture the actual local project, two draft jobs, and exported XML."""
import argparse
import html
import http.cookiejar
import json
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from cvat_local_setup import ROOT


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--session-file',required=True)
    ap.add_argument('--front-zip',type=Path,default=ROOT/'work/exports/hocvien-front.zip')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'work/screenshots')
    ap.add_argument('--jpeg',action='store_true',help='Ảnh JPEG gọn để chèn trực tiếp vào báo cáo')
    args=ap.parse_args()
    state=json.loads((ROOT/'work/cvat_state.json').read_text())
    base=state['base_url']
    if base != 'http://localhost:8080':
        raise SystemExit('Evidence script chỉ dùng CVAT localhost:8080')
    jar=http.cookiejar.MozillaCookieJar(args.session_file); jar.load(ignore_discard=True)
    dest=args.output_dir; dest.mkdir(parents=True,exist_ok=True)
    ext='jpg' if args.jpeg else 'png'
    image_options={'type':'jpeg','quality':80} if args.jpeg else {}
    result=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(viewport={'width':1600,'height':1100})
        context.add_cookies([{'name':c.name,'value':c.value,'url':base,'secure':False} for c in jar])
        for label,group,frame in [('labels',None,None),('front','front',0),('fisheye','fisheye',2)]:
            page=context.new_page(); errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            if group:
                task=state['tasks'][group]
                url=f"{base}/tasks/{task['id']}/jobs/{task['jobs'][0]}?frame={frame}"
            else:
                url=state['project_url']
            page.goto(url,wait_until='networkidle',timeout=60000)
            if group:
                page.locator('.cvat-canvas-container').wait_for(timeout=45000)
            page.screenshot(path=str(dest/f'{label}.{ext}'),full_page=True,**image_options)
            result.append({'view':label,'url':page.url,'page_errors':errors})
            if group=='fisheye':
                page.mouse.move(865,565); page.mouse.wheel(0,-450)
                page.wait_for_timeout(300)
                page.screenshot(path=str(dest/f'fisheye-zoom.{ext}'),full_page=True,**image_options)
            page.close()
        with zipfile.ZipFile(args.front_zip) as zf:
            xml=zf.read('annotations.xml').decode()
        start=xml.index('<image '); end=xml.index('</image>',start)+len('</image>')
        snippet=xml[start:end]
        page=context.new_page()
        page.set_content('<h2>CVAT for images 1.1 — actual exported A01 XML</h2><pre style="font:15px/1.4 monospace;white-space:pre-wrap">'+html.escape(snippet)+'</pre>')
        page.screenshot(path=str(dest/f'xml.{ext}'),full_page=True,**image_options)
        page.close(); browser.close()
    (dest/'browser_verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
