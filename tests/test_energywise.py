"""EnergyWise automated tests. Run from the project folder:  python -m pytest -v"""
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))
import energywise_core as core  # noqa: E402
import app  # noqa: E402


@pytest.fixture(scope='module')
def df():
    return core.load_data()


@pytest.fixture(scope='module')
def model_meta():
    return core.load_model()


# ---------------------------------------------------------------- data
def test_dataset_shape_and_columns(df):
    assert df.shape == (768, 10)
    assert list(df.columns) == list(core.COLUMNS.values())
    assert len(core.FEATURES) == 8 and core.TARGET == 'heating_load'


def test_no_missing_values_and_numeric(df):
    assert int(df.isnull().sum().sum()) == 0
    assert all(np.issubdtype(t, np.number) for t in df.dtypes)


def test_csv_matches_official_xlsx(df):
    with zipfile.ZipFile(core.RAW_ZIP) as z, z.open('ENB2012_data.xlsx') as f:
        raw = pd.read_excel(f).dropna(how='all').dropna(axis=1, how='all')
    raw = raw[list(core.COLUMNS)].rename(columns=core.COLUMNS).reset_index(drop=True)
    pd.testing.assert_frame_equal(raw, df, check_dtype=False)


def test_twelve_building_shapes(df):
    assert len(core.building_shapes(df)) == 12


def test_cooling_load_not_a_feature():
    assert 'cooling_load' not in core.FEATURES


# ---------------------------------------------------------------- model
def test_split_is_reproducible_and_disjoint(df):
    a = core.split(df); b = core.split(df)
    assert list(a[0].index) == list(b[0].index)
    assert not set(a[0].index) & set(a[1].index)
    assert (len(a[0]), len(a[1])) == (614, 154)


def test_saved_metadata_matches_fresh_training(df, model_meta, tmp_path, monkeypatch):
    _, meta = model_meta
    # retrain into a temporary folder and compare metrics with the saved metadata
    monkeypatch.setattr(core, 'MODEL_PATH', tmp_path / 'm.joblib')
    monkeypatch.setattr(core, 'META_PATH', tmp_path / 'm.json')
    fresh = core.train_and_save(df)
    for part in ('train_metrics', 'test_metrics'):
        for k, v in meta[part].items():
            assert fresh[part][k] == pytest.approx(v, abs=1e-12)


def test_model_quality_is_reasonable(model_meta):
    _, meta = model_meta
    assert meta['test_metrics']['R2'] > 0.85          # sanity floor, not a tuned target
    assert abs(meta['train_metrics']['R2'] - meta['test_metrics']['R2']) < 0.05   # no strong overfitting


def test_tampered_model_is_refused(tmp_path, monkeypatch):
    m, j = tmp_path / 'm.joblib', tmp_path / 'm.json'
    shutil.copy(core.MODEL_PATH, m); shutil.copy(core.META_PATH, j)
    with open(m, 'ab') as f:
        f.write(b'tamper')
    monkeypatch.setattr(core, 'MODEL_PATH', m); monkeypatch.setattr(core, 'META_PATH', j)
    with pytest.raises(ValueError, match='hash'):
        core.load_model()


# ---------------------------------------------------------------- tahmin_et()
def scripted(answers):
    it = iter(answers)
    return lambda prompt='': next(it)


def test_tahmin_et_valid_input(df, model_meta, capsys):
    model, meta = model_meta
    pred, row = app.tahmin_et(model, meta, core.building_shapes(df), scripted(['1', '2', '0,25', '3']))
    expected = model.predict(pd.DataFrame([row])[core.FEATURES])[0]
    assert pred == pytest.approx(expected)
    assert 'Tahmini ısıtma yükü' in capsys.readouterr().out


def test_tahmin_et_rejects_bad_input_then_accepts(df, model_meta, capsys):
    model, meta = model_meta
    answers = ['abc', '13', '1', '7', '2', '0.9', '0.10', '9', '1']
    pred, row = app.tahmin_et(model, meta, core.building_shapes(df), scripted(answers))
    out = capsys.readouterr().out
    assert 'bir sayı değil' in out and 'aralığında olmalı' in out and 'Geçerli değerler' in out
    assert row['glazing_area'] == 0.10 and row['glazing_area_distribution'] == 1


def test_zero_glazing_forces_distribution_zero(df, model_meta):
    model, meta = model_meta
    _, row = app.tahmin_et(model, meta, core.building_shapes(df), scripted(['4', '5', '0']))
    assert row['glazing_area_distribution'] == 0


def test_q_exits(df, model_meta):
    model, meta = model_meta
    with pytest.raises(app.Exit):
        app.tahmin_et(model, meta, core.building_shapes(df), scripted(['q']))


# ---------------------------------------------------------------- end-to-end console run
def test_app_end_to_end_subprocess():
    stdin = '1\n1\n2\n0,25\n3\n2\nx\nq\n'
    r = subprocess.run([sys.executable, str(ROOT / 'app.py')], input=stdin, capture_output=True,
                       text=True, encoding='utf-8', cwd=ROOT, timeout=120, env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
    assert r.returncode == 0, r.stderr
    assert 'Tahmini ısıtma yükü' in r.stdout and 'Lütfen 1, 2 veya q girin' in r.stdout and 'Görüşmek üzere' in r.stdout
