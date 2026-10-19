"""EnergyWise core: data loading/validation, model training and safe model loading.

Author: Tugay Sinan Ergün (GitHub: TCoderr)
Data: UCI Machine Learning Repository - Energy Efficiency (Tsanas & Xifara, 2012), CC BY 4.0,
      https://doi.org/10.24432/C51307 . The values come from building energy SIMULATIONS (Ecotect),
      not from measurements of real buildings.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
RAW_ZIP = ROOT / 'data' / 'raw' / 'energy_efficiency.zip'
CSV_PATH = ROOT / 'data' / 'energy_efficiency.csv'
MODEL_PATH = ROOT / 'models' / 'energywise_linear_regression.joblib'
META_PATH = ROOT / 'models' / 'model_metadata.json'
UCI_ZIP_URL = 'https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip'

# original UCI codes -> readable column names
COLUMNS = {
    'X1': 'relative_compactness', 'X2': 'surface_area', 'X3': 'wall_area', 'X4': 'roof_area',
    'X5': 'overall_height', 'X6': 'orientation', 'X7': 'glazing_area', 'X8': 'glazing_area_distribution',
    'Y1': 'heating_load', 'Y2': 'cooling_load',
}
FEATURES = list(COLUMNS.values())[:8]
TARGET = 'heating_load'          # Y1. cooling_load (Y2) is a second target and is never used as an input.
TEST_SIZE = 0.2
RANDOM_STATE = 42


def build_csv_from_zip(zip_path: Path = RAW_ZIP, csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """Convert the official ENB2012_data.xlsx to CSV with readable column names. Values are not changed."""
    with zipfile.ZipFile(zip_path) as z, z.open('ENB2012_data.xlsx') as f:
        raw = pd.read_excel(f)
    raw = raw.dropna(how='all').dropna(axis=1, how='all')      # the sheet can carry empty trailing rows/columns
    missing = [c for c in COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(f'unexpected source columns, missing {missing}')
    df = raw[list(COLUMNS)].rename(columns=COLUMNS)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df


def load_data(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """Read the CSV and fail loudly if its structure is not what the model expects."""
    df = pd.read_csv(csv_path)
    expected = list(COLUMNS.values())
    if list(df.columns) != expected:
        raise ValueError(f'column mismatch: {list(df.columns)}')
    if df[expected].isnull().any().any():
        raise ValueError('dataset contains missing values')
    if not all(np.issubdtype(t, np.number) for t in df.dtypes):
        raise ValueError('all columns must be numeric')
    return df


def split(df: pd.DataFrame):
    X, y = df[FEATURES], df[TARGET]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)


def metrics(y_true, y_pred) -> dict:
    return {'MAE': float(mean_absolute_error(y_true, y_pred)),
            'RMSE': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'R2': float(r2_score(y_true, y_pred))}


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def train_and_save(df: pd.DataFrame | None = None) -> dict:
    """Train LinearRegression on the training split only, evaluate on train and test, save model + metadata."""
    df = load_data() if df is None else df
    X_train, X_test, y_train, y_test = split(df)
    model = LinearRegression().fit(X_train, y_train)     # no scaling: OLS predictions do not depend on feature scale
    meta = {
        'model': 'sklearn.linear_model.LinearRegression',
        'sklearn_version': sklearn.__version__,
        'features': FEATURES, 'target': TARGET,
        'test_size': TEST_SIZE, 'random_state': RANDOM_STATE,
        'n_train': int(len(X_train)), 'n_test': int(len(X_test)),
        'train_metrics': metrics(y_train, model.predict(X_train)),
        'test_metrics': metrics(y_test, model.predict(X_test)),
        'model_score_test_R2': float(model.score(X_test, y_test)),
        'intercept': float(model.intercept_),
        'coefficients': dict(zip(FEATURES, map(float, model.coef_))),
        'feature_ranges': {c: [float(df[c].min()), float(df[c].max())] for c in FEATURES},
        'data_sha256': sha256(CSV_PATH) if CSV_PATH.exists() else None,
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    meta['model_sha256'] = sha256(MODEL_PATH)
    META_PATH.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    return meta


def load_model():
    """Load the saved model only if it is the exact file this project wrote (sha256 + sklearn version check).
    joblib/pickle can execute code, so an unknown or modified model file is never loaded."""
    if not MODEL_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError('model files missing - run: python src/train_model.py')
    meta = json.loads(META_PATH.read_text(encoding='utf-8'))
    if sha256(MODEL_PATH) != meta.get('model_sha256'):
        raise ValueError('model file hash does not match metadata - refusing to load; retrain with src/train_model.py')
    if meta.get('sklearn_version') != sklearn.__version__:
        raise ValueError(f"model trained with scikit-learn {meta.get('sklearn_version')}, installed {sklearn.__version__}; retrain")
    return joblib.load(MODEL_PATH), meta


def building_shapes(df: pd.DataFrame) -> pd.DataFrame:
    """The 12 simulated building geometries (X1-X5 always occur together in the dataset)."""
    geo = ['relative_compactness', 'surface_area', 'wall_area', 'roof_area', 'overall_height']
    shapes = df[geo].drop_duplicates().sort_values('relative_compactness', ascending=False).reset_index(drop=True)
    shapes.index = shapes.index + 1
    return shapes
