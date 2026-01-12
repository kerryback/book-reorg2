import os
import json
import subprocess
import re

# subprocess.run("rm ../book-published-code/*.ipynb")

image_path = "https://www.dropbox.com/scl/fi/6hwvdff7ajaafmkpmnp0o/under_construction.jpg?rlkey=3dex2dx86anniqoutwyqashnu&dl=1"
construction_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        f'<img src="{image_path}" alt="Under Construction" width="400"/>\n'
    ]
}

def has_python_chunks(qmd_file):
    """Check if a .qmd file contains any Python code chunks."""
    try:
        with open(qmd_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for ```{python} blocks
        return bool(re.search(r'```\{python\}', content))
    except FileNotFoundError:
        return False

# Read chapters from _quarto.yml
with open("_quarto.yml", "r") as f:
    lines = [
        line for line in f.readlines()
        if line.strip().startswith("- Chapter")
    ]
chapters = [line.strip()[2:] for line in lines]

# Filter chapters to only those with Python code
print(f"Found {len(chapters)} chapters in _quarto.yml")
chapters = [c for c in chapters if has_python_chunks(c)]
print(f"Processing {len(chapters)} chapters with Python code")

numbers = [f"0{n}" for n in range(1, 10)] + [str(n) for n in range(10, len(chapters) + 1)]
names = [c.split("_")[1].replace("qmd", "ipynb") for c in chapters]
notebooks_out = [number + "_" + name for number, name in zip(numbers, names)]

notebooks_in = [c.replace("qmd", "ipynb") for c in chapters]

for chapter, notebook_in, notebook_out in zip(chapters, notebooks_in, notebooks_out):
    print(f"Converting {chapter}...")
    subprocess.run("quarto convert " + chapter, shell=True, check=True)
    with open(notebook_in, 'r') as f:
        js = json.load(f)

    js['cells'] = [cell for cell in js['cells'] if cell['cell_type'] != 'markdown']

    for cell in js['cells']:
        cell['source'] = [line for line in cell['source'] if not line.strip().startswith('#|')]

    new_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
            "---\n",
            "\n",
            "Created for [Pricing and Hedging Derivative Securities: Theory and Methods](https://book.derivative-securities.org/)\n",
            "\n",
            "Authored by\n",
            "- Kerry Back, Rice University\n",
            "- Hong Liu, Washington University in St. Louis\n",
            "- Mark Loewenstein, University of Maryland\n",
            " \n",
            "---\n",
            "\n",
            f"<a target=\"_blank\" href=\"https://colab.research.google.com/github/math-finance-book/book-code/blob/main/{notebook_out}\">\n",
            "  <img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/>\n",
            "</a>"
    ]
    }
    js['cells'].insert(0, new_cell)
    with open("../book-published-code/" + notebook_out, 'w') as f:
        json.dump(js, f, indent=2)
    os.remove(notebook_in)

# Add and commit new notebooks
print("\nCommitting notebooks...")
subprocess.run("git -C ../book-published-code add .", shell=True, check=True)
result = subprocess.run('git -C ../book-published-code commit -m "update notebooks"', shell=True)

if result.returncode == 0:
    print("Pushing to remote...")
    subprocess.run("git -C ../book-published-code push origin main", shell=True, check=True)
    print("Done!")
else:
    print("No changes to commit.")