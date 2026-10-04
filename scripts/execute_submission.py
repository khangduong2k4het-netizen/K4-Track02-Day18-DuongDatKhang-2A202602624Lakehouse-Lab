"""Execute source notebooks and preserve real cell outputs for submission."""
from pathlib import Path
import sys
import jupytext
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'submission' / 'notebooks'
OUT.mkdir(parents=True, exist_ok=True)
for source in sorted((ROOT / 'notebooks').glob('[0-9]*.py')):
    print(f'Executing {source.name}', flush=True)
    nb = jupytext.read(source)
    nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
    client = NotebookClient(nb, timeout=1200, resources={'metadata': {'path': str(ROOT / 'notebooks')}}, kernel_name='python3')
    client.execute()
    nbformat.write(nb, OUT / (source.stem + '.ipynb'))
    nbformat.write(nb, source.with_suffix('.ipynb'))
    print(f'Saved {source.stem}', flush=True)
