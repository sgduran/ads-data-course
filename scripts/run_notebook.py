"""Execute the course notebook from its expected directory and save fresh outputs."""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "notebooks" / "01_explore_taobao_ads.ipynb"
notebook = nbformat.read(path, as_version=4)
for cell in notebook.cells:
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None

client = NotebookClient(
    notebook, timeout=1800, kernel_name="python3",
    resources={"metadata": {"path": str(path.parent)}},
)
client.execute()
nbformat.write(notebook, path)
print(f"Executed {sum(c.cell_type == 'code' for c in notebook.cells)} code cells: {path}")
