"""Build the three role-specific guides with original, native-cropped images."""
from pathlib import Path
import re
import json
import build_handouts as base

ROOT = Path(__file__).parent
base.OUT = ROOT / 'guides'
base.OUT.mkdir(exist_ok=True)
BUILD = ROOT / '.build' / 'manuscripts'
BUILD.mkdir(parents=True, exist_ok=True)
base.CROPS.update({
    'v2-environment.png': (0, 62, 940, 211),
    'v2-rtl.png': (0, 62, 910, 212),
    'v2-simulation-pass.png': (0, 62, 1225, 214),
    'v2-failure.png': (0, 62, 1225, 448),
    'v2-dv-schematic.png': (22, 95, 1214, 490),
    'v2-dv-timing-dialog.png': (338, 116, 544, 496),
    'v2-dv-timing-report.png': (22, 52, 1214, 653),
    'v2-verdi-overview.png': (0, 52, 1237, 697),
    'v2-verdi-waveform.png': (0, 441, 1237, 306),
    'v2-icc2-floorplan.png': (0, 52, 1237, 691),
    'v2-coverage.png': (0, 95, 1237, 695),
})

if __name__ == '__main__':
    common = (ROOT / 'manuscripts/common-access.md').read_text()
    code_links = json.loads((ROOT / 'manuscripts/code-links.json').read_text())
    for name in ('verification', 'pd', 'rtl'):
        text = (ROOT / 'manuscripts' / (name+'.md')).read_text()
        text = text.replace('{{ACCESS}}', common)
        links = '\n\n'.join(label + ': https://github.com/abhinavnandwani/cae-synopsys-guides/blob/main/' + path for label, path in code_links[name])
        text = text.replace('{{CODE_LINKS}}', links)
        if re.search(r'\{\{[A-Z_]+\}\}', text):
            raise ValueError('Unresolved section in '+name)
        target = BUILD / ('cae-'+name+'-handout.md')
        target.write_text(text)
        base.make_doc(target)
