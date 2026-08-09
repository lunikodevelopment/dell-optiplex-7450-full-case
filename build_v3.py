from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "source_parts"
fragments = sorted(PARTS.glob("part_*.pyfrag"))
if not fragments:
    raise SystemExit("No source fragments found in source_parts/")

source = "".join(p.read_text(encoding="utf-8") for p in fragments)
source = source.replace(
    "OUT=Path('/mnt/data/dell_7450_full_case_v3')",
    "OUT=Path.cwd() / 'generated'",
    1,
)

assembled = ROOT / "CAD_SOURCE_make_v3.py"
assembled.write_text(source, encoding="utf-8")
print(f"Assembled {assembled}")
print("Generating CAD into ./generated ...")
exec(compile(source, str(assembled), "exec"), {"__name__": "__main__", "__file__": str(assembled)})
