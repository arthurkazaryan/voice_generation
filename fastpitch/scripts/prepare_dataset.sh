#!/usr/bin/env bash

set -e

for SPK in triple; do
  export DATA_DIR=/windows/TTSDatasets/ru/${SPK}

  python3 -u prepare_dataset.py \
      --wav-text-filelists $DATA_DIR/metadata_embed_stress_phonemes_22k.csv \
      --n-workers 6 \
      --batch-size 1 \
      --dataset-path $DATA_DIR \
      --extract-pitch \
      --f0-method pyin
done
