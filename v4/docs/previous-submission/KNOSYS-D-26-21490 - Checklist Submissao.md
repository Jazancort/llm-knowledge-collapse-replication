# KNOSYS-D-26-21490 — Checklist de Submissão
Data: 2026-10-04 | HEAD: ver git log

## Pacote gerado
- [x] Manuscrito rastreado (highlights azul): KNOSYS-D-26-21490 - Manuscript Revised Tracked - 2026-10-04.pdf
- [x] Manuscrito limpo (showchangesfalse): KNOSYS-D-26-21490 - Manuscript Revised - 2026-10-04.pdf
- [x] Carta ponto a ponto: KNOSYS-D-26-21490 - Response to Reviewers - 2026-10-04.pdf
- [ ] Cover letter (Word) — pendente se solicitado pelo EES
- [ ] CRediT, Author Agreement, Declaration of Interest — via EES
- [ ] Figuras em formato não-PDF 300 dpi — verificar se EES exige

## Alinhamentos confirmados (manuscrito × carta)
- [x] K0 = conjunto, |K0| = cardinalidade, R(t) fração
- [x] SDI-3: D1=Distinct-1, ΔI=Instab(T)-Instab(1), MeanLen_t na geração t
- [x] G5: 2/3 qualitative ordering, Pi não reportado, sem backbone inédito
- [x] NF4 r16 ≠ bf16 r16 (pipelines diferentes, 96.2% vs 97.4%)
- [x] G4: seed E ordem variam juntos; p=0.70 não isola ordem
- [x] Gemma3 r>=10 (não r>=16)
- [x] r=256 = lowest-pressure degradative (não "boundary")
- [x] r=128/r=256 = r128 bounded + r256 degradative (não "two above-threshold")
- [x] TCE citado em Related Work (não ausente)
- [x] C2-C5 arquivados no replication repository (não Appendix A)
- [x] 27 runs (não 23)
- [x] v1.0.3 = scripts iniciais; scripts revisados em release futuro
- [x] Slope B7 0%=-1.13 pp/gen, 50%=-0.15 pp/gen (da fonte, N=5 seeds)
- [x] GoneSlope=-1.20 (N=6 seeds), GtwoSlope=-0.91 (ambos os braços)
- [x] G2 = ganho de retenção sem redução de slope (near-arrest removido)

## Números B7 vigentes (commit 6fd9145+)
| Dose | Gen5 Δ | Gen10 Δ | IC 95% | p |
|------|--------|---------|--------|---|
| 10%  | +3.6pp | +1.8pp  | [-1.1,4.7] | 0.160 ns |
| 25%  | +3.8pp | +4.9pp  | [2.5,7.2]  | 0.005 |
| 50%  | +4.4pp | +9.2pp  | [6.9,11.6] | <0.001 |
