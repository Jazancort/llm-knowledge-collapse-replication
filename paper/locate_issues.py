import sys
sys.stdout.reconfigure(encoding='utf-8')

ms = r"G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)\v4\manuscript\manuscript-anonymous.tex"

with open(ms, encoding='utf-8') as f:
    lines = f.readlines()

checks = [
    ('thumbnail/cas-email', lambda l: 'thumbnail' in l.lower() or 'cas-email' in l.lower()),
    ('GoneFour comma', lambda l: 'GoneFour' in l and ('\\pm' not in l) and (',' in l)),
    ('SHA-1', lambda l: 'sha' in l.lower()),
    ('tenfold', lambda l: 'tenfold' in l.lower() or 'ten-fold' in l.lower()),
    ('Fig11/etp_framework', lambda l: 'etp_framework' in l or 'fig11' in l.lower() or 'fig:11' in l.lower() or ('fig' in l.lower() and '11' in l)),
    ('-0.91 arms', lambda l: '0.91' in l and 'arm' in l.lower()),
    ('SHA or hash weight', lambda l: ('sha' in l.lower() or 'hash' in l.lower()) and ('weight' in l.lower() or 'identical' in l.lower() or 'checkpoint' in l.lower())),
    ('identical weights', lambda l: 'identical' in l.lower() and 'weight' in l.lower()),
    ('3.3 section', lambda l: 'subsection' in l.lower() and ('3.3' in l or 'reprod' in l.lower() or 'checkp' in l.lower())),
]

for label, fn in checks.items() if hasattr(checks, 'items') else [(l,f) for l,f in checks]:
    print(f'\n=== {label} ===')
    for i, line in enumerate(lines, 1):
        try:
            if fn(line):
                print(f'L{i}: {line.rstrip()}')
        except Exception:
            pass
