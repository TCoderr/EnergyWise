"""EnergyWise - terminal application: predicts the heating load of a building from its architectural features.

Author: Tugay Sinan Ergün (GitHub: TCoderr)
Run from the project folder:  python app.py
The model is a LinearRegression trained on simulated data (UCI Energy Efficiency, CC BY 4.0). Predictions are
estimates for buildings similar to the 12 simulated shapes, not measurements of a real building.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
import pandas as pd  # noqa: E402

import energywise_core as core  # noqa: E402


class Exit(Exception):
    """Raised when the user types q at any prompt."""


def ask_number(ask, prompt, low, high, integer=False, allowed=None):
    """Ask until the user types a valid number in [low, high] (or one of `allowed`). 'q' exits."""
    while True:
        raw = ask(prompt).strip().lower()
        if raw in ('q', 'çıkış', 'cikis', 'exit'):
            raise Exit
        try:
            value = float(raw.replace(',', '.'))
        except ValueError:
            print(f'  ! "{raw}" bir sayı değil. Lütfen {low}–{high} arasında bir değer girin (çıkmak için q).')
            continue
        if integer and not value.is_integer():
            print('  ! Lütfen tam sayı girin.')
            continue
        if allowed is not None and value not in allowed:
            print(f'  ! Geçerli değerler: {", ".join(str(int(a)) for a in allowed)}.')
            continue
        if not low <= value <= high:
            print(f'  ! Değer {low}–{high} aralığında olmalı (veri setinde görülen aralık).')
            continue
        return int(value) if integer else value


def show_shapes(shapes):
    print('\n  Veri setindeki 12 simüle bina tipi (geometri):')
    print(f"  {'No':>3}  {'Kompaktlık':>10}  {'Yüzey':>7}  {'Duvar':>7}  {'Çatı':>7}  {'Yükseklik':>9}")
    for no, r in shapes.iterrows():
        print(f"  {no:>3}  {r.relative_compactness:>10.2f}  {r.surface_area:>7.1f}  {r.wall_area:>7.1f}"
              f"  {r.roof_area:>7.2f}  {r.overall_height:>9.1f}")


def tahmin_et(model, meta, shapes, ask=input):
    """Ask the user for a building, validate every input and return (prediction, inputs)."""
    r = meta['feature_ranges']
    show_shapes(shapes)
    no = ask_number(ask, f'\nBina tipi numarası (1–{len(shapes)}): ', 1, len(shapes), integer=True)
    orientation = ask_number(ask, 'Yön kodu (2, 3, 4 veya 5): ', 2, 5, integer=True, allowed={2, 3, 4, 5})
    glazing = ask_number(ask, f"Cam alanı oranı ({r['glazing_area'][0]:.2f}–{r['glazing_area'][1]:.2f}, ör. 0,25): ",
                         r['glazing_area'][0], r['glazing_area'][1])
    if glazing == 0:
        distribution = 0
        print('  Cam alanı 0 olduğu için cam dağılım kodu 0 alındı (veri setinde de böyledir).')
    else:
        distribution = ask_number(ask, 'Cam dağılım kodu (1–5): ', 1, 5, integer=True)
    row = shapes.loc[no].to_dict()
    row.update(orientation=orientation, glazing_area=glazing, glazing_area_distribution=distribution)
    X = pd.DataFrame([row])[core.FEATURES]
    prediction = float(model.predict(X)[0])
    mae = meta['test_metrics']['MAE']
    print(f'\n>>> Tahmini ısıtma yükü: {prediction:.2f}  (test kümesinde ortalama mutlak hata ≈ {mae:.2f})')
    print(f'    Girdiler: bina tipi {no}, yön {orientation}, cam oranı {glazing:.2f}, dağılım {distribution}.')
    print('    Not: Simülasyon verisinden öğrenilmiş bir tahmin; birim UCI sayfasında verilmemiş.')
    return prediction, row


def main(ask=input):
    print('=' * 64)
    print(' EnergyWise — Bina Isıtma Yükü Tahmini (Linear Regression)')
    print('=' * 64)
    try:
        model, meta = core.load_model()
    except (FileNotFoundError, ValueError) as e:
        print(f'Model yüklenemedi: {e}')
        print('Modeli yeniden oluşturmak için:  python src/train_model.py')
        return 1
    shapes = core.building_shapes(core.load_data())
    while True:
        try:
            choice = ask('\n[1] Tahmin yap   [2] Bina tiplerini göster   [q] Çıkış\nSeçiminiz: ').strip().lower()
            if choice in ('q', 'çıkış', 'cikis', 'exit'):
                break
            if choice == '1':
                tahmin_et(model, meta, shapes, ask)
            elif choice == '2':
                show_shapes(shapes)
            else:
                print('  ! Lütfen 1, 2 veya q girin.')
        except Exit:
            break
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print('Görüşmek üzere!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
