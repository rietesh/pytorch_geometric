from pathhlib import Path

modules = Path(__file__).parent.rglob('*.py')
__all__ = [
    Path(f).parts[-1][:-3] for f in modules
    if Path(f).is_file() and not f.parts[-1].endswith('__init__.py')
]
