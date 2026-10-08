#!/usr/bin/env bash
set -euo pipefail
cd ~/scratch/llm-knowledge-collapse

export CUDA_VISIBLE_DEVICES=1
LOG_DIR="outputs/revisao_final_logs"
GEMMA="google/gemma-3-1b-it"
mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_DIR/master.log"; }

run_exp() {
    local name="$1"; shift
    log "START  $name"
    if uv run python scripts/g1_rank_ablation.py "$@" >> "$LOG_DIR/${name}.log" 2>&1; then
        log "DONE   $name (exit 0)"
    else
        log "FAIL   $name (exit $?)"
    fi
}

log "=== CONTINUACAO v3 ==="

# G2: Gemma3 r=10 — seeds 137+256 todas doses, seed15 doses 10/25/50%
log "--- G2: Gemma3 r=10 restantes ---"
for SEED in 137 256; do
    for DOSE in 0.00 0.10 0.25 0.50; do
        DTAG=$(python3 -c "print(int($DOSE*100))")
        run_exp "G2_gemma_r10_s${SEED}_dose${DTAG}" \
            --model $GEMMA --rank 10 --seed $SEED --dose $DOSE \
            --tag "_G2_dose${DTAG}" --generations 10
    done
done
for DOSE in 0.10 0.25 0.50; do
    DTAG=$(python3 -c "print(int($DOSE*100))")
    run_exp "G2_gemma_r10_s15_dose${DTAG}" \
        --model $GEMMA --rank 10 --seed 15 --dose $DOSE \
        --tag "_G2_dose${DTAG}" --generations 10
done

# G3: Qwen bf16 sem NF4
log "--- G3: Qwen bf16 no-NF4 ---"
for SEED in 15 137 256; do
    run_exp "G3_qwen_r16_s${SEED}_bf16" \
        --rank 16  --seed $SEED --no-quant --tag "_G3_bf16_r16"  --generations 10
    run_exp "G3_qwen_r256_s${SEED}_bf16" \
        --rank 256 --seed $SEED --no-quant --tag "_G3_bf16_r256" --generations 10
done

# G4: Qwen r=256 variância de ordem
log "--- G4: Qwen r=256 seeds 42/101/202 ---"
for SEED in 42 101 202; do
    run_exp "G4_qwen_r256_s${SEED}_ordem" \
        --rank 256 --seed $SEED --tag "_G4_ordem_s${SEED}" --generations 10
done

# G5: Pi prospectivo
log "--- G5: Pi prospectivo ---"
run_exp "G5_qwen_r128_s15_lr5e6" --rank 128 --seed 15 --lr 5e-6  --tag "_G5_lr5e6"     --generations 5
run_exp "G5_qwen_r128_s15_lr2e5" --rank 128 --seed 15 --lr 2e-5  --tag "_G5_lr2e5"     --generations 5
run_exp "G5_qwen_r32_s15_lr2e5"  --rank 32  --seed 15 --lr 2e-5  --tag "_G5_lr2e5_r32" --generations 5

log "=== CONTINUACAO v3 CONCLUIDA ==="
