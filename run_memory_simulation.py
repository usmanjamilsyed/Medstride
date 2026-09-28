"""Run the supplied Part 2 notebook as a standalone CPU simulation."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/memory-simulation"))
    args = parser.parse_args()
    notebook = Path(__file__).resolve().parent / "notebooks" / "part2.ipynb"
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cells = json.loads(notebook.read_text())["cells"]
    namespace = {"__name__": "__main__"}
    previous_dir = Path.cwd()
    completed = 0
    try:
        os.chdir(output)
        for index, cell in enumerate(cells):
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                exec(compile(source, f"{notebook.name}:cell-{index}", "exec"), namespace)
                completed += 1
        for name in ("ablation_summary_df", "persistence_table", "duration_summary",
                     "ttl_summary", "bias_summary", "utility_summary", "boundary_summary"):
            namespace[name].to_csv(output / f"{name}.csv", index=False)
        (output / "run-status.json").write_text(json.dumps({"completed_code_cells": completed,
            "seed": namespace["SEED"], "episodes": len(namespace["episodes"]),
            "data": "synthetic"}, indent=2) + "\n")
    finally:
        os.chdir(previous_dir)
    print(f"Completed {completed} code cells. Outputs: {output}")


if __name__ == "__main__":
    main()
