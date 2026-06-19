"""Dynamically generate the src/xtce_lib/xtce/__init__.py file."""

import ast
from pathlib import Path


def generate_xtce_init(directory_path: Path) -> None:
    """Generate the xtce/__init__.py file."""
    target_dir = Path(directory_path)
    init_file = target_dir / "__init__.py"

    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {target_dir}")

    modules: dict[str, list[str]] = {}
    all_classes: list[str] = []

    # Parse all py files in the directory
    for file_path in sorted(target_dir.glob("*.py")):
        if file_path.name == "__init__.py":
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            # Extract top-level classes
            classes = sorted(
                [
                    node.name
                    for node in tree.body
                    if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
                ]
            )

            if classes:
                modules[file_path.stem] = classes
                all_classes.extend(classes)

        except SyntaxError as e:
            print(f"Syntax error in {file_path.name}, skipping: {e}")

    # Build the __init__.py content
    lines = ['"""Unified XTCE model module."""', "", "from typing import Any", ""]

    # Build the import blocks
    for module_name, class_names in modules.items():
        lines.append(f"from .{module_name} import (")
        for cls in class_names:
            lines.append(f"    {cls},")
        lines.append(")")

    # Build the __all__ block
    lines.append("")
    lines.append("__all__ = [")
    for cls in all_classes:
        lines.append(f'    "{cls}",')
    lines.append("]")
    lines.append("")

    # Append the Pydantic rebuild logic
    rebuild_logic = '''
def _rebuild_all_models(
    base_class: type[XtceBaseModel], namespace: dict[str, Any]
) -> None:
    """Recursively find and rebuild all Pydantic models.

    This resolves forward references for all models in the module.
    """
    for subclass in base_class.__subclasses__():
        try:
            subclass.model_rebuild(_types_namespace=namespace)
            _rebuild_all_models(subclass, namespace)
        except Exception as e:
            raise RuntimeError(
                f"Error rebuilding model {subclass.__name__}: {e}"
            ) from e

_rebuild_all_models(XtceBaseModel, globals())
'''
    lines.append(rebuild_logic.strip() + "\n")

    # Write the file
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {init_file} with {len(all_classes)} classes exported.")


if __name__ == "__main__":
    generate_xtce_init(Path("src/xtce_lib/xtce"))
