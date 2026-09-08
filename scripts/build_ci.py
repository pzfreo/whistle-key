"""Headless regeneration of the MCP-authored model for CI and export checks."""
import argparse
import json
from pathlib import Path
import runpy

from build123d import export_step, export_stl

ROOT = Path(__file__).resolve().parents[1]


def load_model(model_name="single_key"):
    """Supply the two inspection helpers normally provided by the MCP session."""
    def show(shape, name=None):
        if name:
            shape.label = name

    def measure(shape):
        return {"volume": shape.volume, "topology": {"faces": len(shape.faces())}}

    return runpy.run_path(
        str(ROOT / "scripts" / f"{model_name}.py"),
        init_globals={"show": show, "measure": measure},
    )


def build(output, model_name="single_key"):
    output.mkdir(parents=True, exist_ok=True)
    model = load_model(model_name)
    report = {}
    for name, part in model["print_parts"].items():
        if not part.is_valid or len(part.solids()) != 1 or part.volume <= 0:
            raise ValueError(f"Invalid printable solid: {name}")
        export_step(part, str(output / f"{name}.step"))
        export_stl(part, str(output / f"{name}.stl"))
        report[name] = {"volume_mm3": part.volume, "faces": len(part.faces())}
    export_step(model["assembly"], str(output / "assembly-open.step"))
    (output / "geometry-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Exported {len(report)} printable parts and assembly to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    parser.add_argument("--model", choices=["single_key", "three_key"], default="single_key")
    args=parser.parse_args()
    build(args.output, args.model)
