import importlib.abc
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

PGA_DIR = Path(__file__).resolve().parent.parent

_BARE_MODULES = [
    "canonical_evidence",
    "config",
    "extractors",
    "graph",
    "models",
    "preprocess",
    "prompt_generator",
    "prompts",
    "report_discovery",
    "state",
    "utils",
    "validator",
]


class _PgaBareModuleFinder(importlib.abc.MetaPathFinder):
    # Other services (e.g. SDR's seo tools) mutate sys.path at import time and
    # own same-named top-level modules (prompt_generator, prompts, validator).
    # A meta_path finder outranks every sys.path entry, pinning these bare
    # names to this service regardless of import order or path pollution.
    _names = set(_BARE_MODULES)

    def find_spec(self, fullname, path=None, target=None):
        if fullname not in self._names:
            return None
        module_file = PGA_DIR / f"{fullname}.py"
        if not module_file.exists():
            return None
        return importlib.util.spec_from_file_location(fullname, module_file)


if not any(isinstance(f, _PgaBareModuleFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _PgaBareModuleFinder())

for _name in _BARE_MODULES:
    sys.modules.pop(_name, None)
