"""Rebuild the CSV from the official UCI zip (if needed), train the model and print its metrics.
Usage (from the project folder):  python src/train_model.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import energywise_core as core  # noqa: E402


def main():
    if not core.CSV_PATH.exists():
        if not core.RAW_ZIP.exists():
            sys.exit(f'Missing {core.RAW_ZIP}. Download it from {core.UCI_ZIP_URL}')
        core.build_csv_from_zip()
        print(f'CSV created: {core.CSV_PATH}')
    meta = core.train_and_save()
    print(json.dumps({k: meta[k] for k in ('n_train', 'n_test', 'train_metrics', 'test_metrics')}, indent=2))
    print(f'Model saved: {core.MODEL_PATH}')


if __name__ == '__main__':
    main()
