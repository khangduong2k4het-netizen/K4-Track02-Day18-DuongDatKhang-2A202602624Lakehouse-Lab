"""Screenshot real executed notebook outputs in a local headless browser."""
from pathlib import Path
import html
import nbformat
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'submission' / 'screenshots'
DEST.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1500, 'height': 1000}, device_scale_factor=1)
    for file in sorted((ROOT / 'submission' / 'notebooks').glob('*.ipynb')):
        nb = nbformat.read(file, 4)
        blocks = []
        for i, cell in enumerate(nb.cells):
            for output in cell.get('outputs', []):
                if output.output_type == 'error':
                    raise RuntimeError(f'{file}: error output')
                if output.output_type == 'stream' and output.get('name') == 'stdout':
                    blocks.append(f'<h3>Cell {i+1} — execution {cell.execution_count}</h3><pre>{html.escape(output.text)}</pre>')
        if file.stem.startswith('01'):
            log = ROOT / '_lakehouse' / 'scratch' / 'users_delta' / '_delta_log'
            blocks.append('<h3>Actual _delta_log directory and first commit JSON</h3><pre>' + html.escape('\n'.join(f.name for f in sorted(log.glob('*.json'))) + '\n\n' + sorted(log.glob('*.json'))[0].read_text(encoding='utf-8')) + '</pre>')
        document = '<!doctype html><meta charset="utf-8"><style>body{font:16px Arial;margin:32px;color:#172033}pre{font:14px Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5fa;padding:18px;border:1px solid #d5dce7}h1{color:#174ea6}</style>'
        document += f'<h1>{file.stem}</h1><p>Browser screenshot of preserved Jupyter execution outputs. Source: submission/notebooks/{file.name}. Local HTML export; not the live Jupyter UI.</p>' + ''.join(blocks)
        target = DEST / (file.stem + '.html')
        target.write_text(document, encoding='utf-8')
        page.goto(target.as_uri())
        page.screenshot(path=str(DEST / (file.stem + '.png')), full_page=True)
        print(f'Captured {file.stem}', flush=True)
    browser.close()
