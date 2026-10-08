"""
make_per_seed_jsons.py — Gera os per-seed JSON files para o pacote de replicação.

Lê resultados_consolidados.csv e escreve um JSON por (group, seed, dose, rank, bf16)
em data/per-seed-results/<group>/<arm_label>/seed_<N>.json

Uso:
    cd v4/
    uv run python scripts/analysis/make_per_seed_jsons.py

Output:
    data/per-seed-results/   (criado se não existir)
      B7/seed_15_dose0.json
      B7/seed_15_dose10.json
      ...
      G1/seed_15.json
      G2/seed_15_dose0.json
      ...
"""
import csv, json, sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).resolve().parents[2]   # paper/
CSV_PATH = BASE / 'docs' / 'revision' / 'resultados' / 'resultados_consolidados.csv'
OUT_DIR  = BASE / 'data' / 'per-seed-results'

if not CSV_PATH.exists():
    print(f"ERRO: CSV não encontrado em {CSV_PATH}")
    sys.exit(1)

# ─── Carregar CSV ──────────────────────────────────────────────────────────────
with open(CSV_PATH, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Carregados {len(rows)} registros de {CSV_PATH.name}")

# ─── Agrupar por (group, seed, dose, rank, bf16, ordem) ───────────────────────
arms = defaultdict(list)
for r in rows:
    group = r['group'].strip() or 'B7'  # grupo vazio = B7
    key = (group, r['seed'], r['dose'], r['rank'], r['bf16'], r['ordem'])
    arms[key].append(r)

print(f"Encontrados {len(arms)} arms únicos")

# ─── Gerar JSONs ───────────────────────────────────────────────────────────────
written = 0
for (group, seed, dose, rank, bf16, ordem), records in sorted(arms.items()):
    # Determinar label do arm (diretório)
    arm_dir = OUT_DIR / group
    arm_dir.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo
    parts = [f"seed_{seed}"]
    if dose and dose != '0':
        parts.append(f"dose{dose}")
    if bf16 == 'True':
        parts.append("bf16")
    if ordem == 'True':
        parts.append("ordem")
    fname = "_".join(parts) + ".json"

    # Ordenar gerações
    records_sorted = sorted(records, key=lambda r: int(r['generation']))

    # Determinar backbone a partir do group e rank
    backbone = "gemma3" if group == "G2" else "qwen"

    # Montar estrutura JSON
    payload = {
        "group": group,
        "backbone": backbone,
        "rank": int(rank) if rank else None,
        "seed": int(seed),
        "dose_pct": int(dose) if dose else 0,
        "bf16": bf16 == 'True',
        "ordem_aleatoria": ordem == 'True',
        "k0": int(records_sorted[0]['k0']) if records_sorted else None,
        "dirname": records_sorted[0]['dirname'] if records_sorted else None,
        "generations": [
            {
                "gen": int(r['generation']),
                "retention": int(r['retention']),
                "retention_pct": float(r['retention_pct']),
                "erank": float(r['erank']) if r.get('erank') else None,
            }
            for r in records_sorted
        ]
    }

    out_path = arm_dir / fname
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    written += 1

print(f"\nEscrito: {written} JSONs em {OUT_DIR}")
print("\nEstrutura criada:")
for group_dir in sorted(OUT_DIR.iterdir()):
    files = sorted(group_dir.iterdir())
    print(f"  {group_dir.name}/  ({len(files)} arquivos)")
    for fp in files[:3]:
        print(f"    {fp.name}")
    if len(files) > 3:
        print(f"    ... +{len(files)-3} mais")
