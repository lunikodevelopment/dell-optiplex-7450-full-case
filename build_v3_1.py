from pathlib import Path

PARTS = Path('source_parts_v3_1')
source = ''.join(p.read_text() for p in sorted(PARTS.glob('part_*.pyfrag')))
source = source.replace("OUT=Path('/mnt/data/dell_7450_full_case_v3_1_clearance')", "OUT=Path('generated')", 1)
Path('CAD_SOURCE_make_v3_1.py').write_text(source)
exec(compile(source, 'CAD_SOURCE_make_v3_1.py', 'exec'), {'__name__': '__main__'})
