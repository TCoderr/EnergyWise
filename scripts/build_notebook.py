"""Generate notebooks/EnergyWise.ipynb (Colab compatible, self-contained). Run: python scripts/build_notebook.py"""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
cells = []

cells += [md("""# EnergyWise — Bina Isıtma Yükü Tahmini

**Eğitim:** Yapay Zeka İçin Basitleştirilmiş Python · **Yazar:** Tugay Sinan Ergün (GitHub: TCoderr)

## 1. Proje Tanım Formu

| Başlık | Açıklama |
|---|---|
| Problem cümlesi | Bir binanın mimari özelliklerinden (kompaktlık, yüzey/duvar/çatı alanı, yükseklik, yön, cam alanı ve dağılımı) **ısıtma yükünü** tahmin et. |
| Hedef değişken | `heating_load` (UCI kodu Y1) |
| Problem türü | Regresyon (sayısal tahmin) |
| Model | `sklearn.linear_model.LinearRegression` |

**Gerekçe:** Tasarım aşamasında bir binanın ne kadar ısıtma enerjisine ihtiyaç duyacağını kabaca bilmek, mimarların ve mühendislerin farklı biçim ve cam seçeneklerini karşılaştırmasına yardımcı olur. Ayrıntılı enerji simülasyonu zaman alır; basit bir model hızlı bir ön tahmin sunabilir.

> **Önemli:** Veri seti gerçek binalardan ölçülmemiştir. UCI açıklamasına göre değerler, Ecotect'te simüle edilen 12 bina şeklinin enerji analizinden üretilmiştir. Bu nedenle sonuçlar simülasyon koşullarına benzeyen binalar için geçerlidir."""),
md("## 2. Kurulum ve veri yükleme\nNotebook önce proje klasöründeki CSV dosyasını arar. Bulamazsa (ör. Google Colab) veriyi **resmî UCI adresinden** indirir. Windows'a özgü bir dosya yolu kullanılmaz."),
code("""import io, json, urllib.request, zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

UCI_ZIP_URL = 'https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip'
COLUMNS = {'X1': 'relative_compactness', 'X2': 'surface_area', 'X3': 'wall_area', 'X4': 'roof_area',
           'X5': 'overall_height', 'X6': 'orientation', 'X7': 'glazing_area', 'X8': 'glazing_area_distribution',
           'Y1': 'heating_load', 'Y2': 'cooling_load'}

candidates = [Path('data/energy_efficiency.csv'), Path('../data/energy_efficiency.csv')]
csv_path = next((p for p in candidates if p.exists()), None)
if csv_path is not None:
    df = pd.read_csv(csv_path)
    print(f'Yerel CSV okundu: {csv_path}')
else:
    raw_zip = urllib.request.urlopen(UCI_ZIP_URL, timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as z, z.open('ENB2012_data.xlsx') as f:
        df = pd.read_excel(f).dropna(how='all').dropna(axis=1, how='all')[list(COLUMNS)].rename(columns=COLUMNS)
    df.to_csv('energy_efficiency.csv', index=False)
    print('Veri resmî UCI adresinden indirildi ve energy_efficiency.csv olarak kaydedildi.')

# grafiklerin kaydedileceği klasör: proje içinde reports/figures, Colab'da ./figures
FIG_DIR = Path('reports/figures') if Path('reports').exists() else (Path('../reports/figures') if Path('../reports').exists() else Path('figures'))
FIG_DIR.mkdir(parents=True, exist_ok=True)
print('Grafik klasörü:', FIG_DIR)"""),
md("## 3. Veriyi tanıma\n`head()`, `shape`, veri tipleri ve eksik değer kontrolü."),
code("df.head()"),
code("print('shape:', df.shape)\nprint('\\nVeri tipleri:')\nprint(df.dtypes)"),
code("""missing = df.isnull().sum()
print('Eksik değer sayıları:'); print(missing)
print('\\nToplam eksik değer:', int(missing.sum()))
print('Tekrarlanan satır sayısı:', int(df.duplicated().sum()))"""),
md("""### Veri sözlüğü

| Sütun | UCI kodu | Tip | Anlamı |
|---|---|---|---|
| relative_compactness | X1 | Sayısal (sürekli) | Göreli kompaktlık: bina biçiminin ne kadar "toplu" olduğunu gösteren oran |
| surface_area | X2 | Sayısal (sürekli) | Toplam dış yüzey alanı |
| wall_area | X3 | Sayısal (sürekli) | Duvar alanı |
| roof_area | X4 | Sayısal (sürekli) | Çatı alanı |
| overall_height | X5 | Sayısal (sürekli) | Toplam bina yüksekliği |
| orientation | X6 | Sayısal kod (kategorik anlamlı) | Binanın yönü; 2–5 arası kod |
| glazing_area | X7 | Sayısal (sürekli) | Cam alanı oranı |
| glazing_area_distribution | X8 | Sayısal kod (kategorik anlamlı) | Cam alanının cephelere dağılımı; 0–5 arası kod |
| heating_load | Y1 | Sayısal (sürekli) | **Hedef:** ısıtma yükü |
| cooling_load | Y2 | Sayısal (sürekli) | Soğutma yükü: ikinci hedef. Girdi olarak **kullanılmaz** (hedefle birlikte üretilen bir çıktıdır) |

UCI sayfasında birim, yön kodlarının ve cam dağılım kodlarının anlamı verilmemiştir. Bu nedenle kodlar burada yorumlanmamıştır."""),
md("## 4. Temizleme\nEksik değer ve tekrarlanan satır yoksa veri değiştirilmez. Değer aralıkları ve kod değerleri kontrol edilir."),
code("""print(df.describe().T[['count', 'mean', 'std', 'min', 'max']].round(3))
print('\\nTemizleme gerekli mi?', 'Hayır: eksik veya tekrarlanan satır yok.' if df.isnull().sum().sum() == 0 and df.duplicated().sum() == 0 else 'Evet')
# veri setinden doğrulanan kural: cam alanı 0 ise cam dağılım kodu da 0
print('glazing_area == 0  <=>  glazing_area_distribution == 0 :', bool(((df.glazing_area == 0) == (df.glazing_area_distribution == 0)).all()))"""),
md("## 5. Keşifçi veri analizi (EDA)\n### 5.1 Özet istatistikler (`describe`) ve kategorik değerler (`value_counts`)"),
code("df.describe().round(2)"),
code("""for c in ['overall_height', 'orientation', 'glazing_area', 'glazing_area_distribution']:
    print(f'--- {c} ---'); print(df[c].value_counts().sort_index()); print()"""),
md("### 5.2 Hedefe göre farklar (`groupby`)"),
code("""by_height = df.groupby('overall_height')['heating_load'].agg(['count', 'mean', 'min', 'max']).round(2)
by_glazing = df.groupby('glazing_area')['heating_load'].agg(['count', 'mean']).round(2)
by_orient = df.groupby('orientation')['heating_load'].agg(['count', 'mean']).round(2)
print('Yüksekliğe göre ısıtma yükü:'); print(by_height, '\\n')
print('Cam alanına göre ortalama ısıtma yükü:'); print(by_glazing, '\\n')
print('Yöne göre ortalama ısıtma yükü:'); print(by_orient)"""),
md("### 5.3 Grafik 1 — Hedef değişkenin dağılımı"),
code("""fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df['heating_load'], bins=30, color='#2E86AB', edgecolor='white')
ax.set_title('Isıtma yükünün dağılımı (768 simüle bina)')
ax.set_xlabel('Isıtma yükü (heating_load)'); ax.set_ylabel('Bina sayısı')
fig.tight_layout(); fig.savefig(FIG_DIR / '01_hedef_dagilimi.png', dpi=150); plt.show()"""),
md("**Yorum:** Dağılım tek bir tepeli değildir; iki ayrı küme görülür. Aşağıdaki grafik, bu iki kümenin bina yüksekliğiyle ilişkili olduğunu gösterir."),
md("### 5.4 Grafik 2 — Göreli kompaktlık ve ısıtma yükü (renk: bina yüksekliği)"),
code("""fig, ax = plt.subplots(figsize=(7, 4))
for h, color in [(3.5, '#F18F01'), (7.0, '#2E86AB')]:
    part = df[df.overall_height == h]
    ax.scatter(part.relative_compactness, part.heating_load, s=14, alpha=0.6, color=color, label=f'Yükseklik {h}')
ax.set_title('Göreli kompaktlık ve ısıtma yükü')
ax.set_xlabel('Göreli kompaktlık (relative_compactness)'); ax.set_ylabel('Isıtma yükü'); ax.legend()
fig.tight_layout(); fig.savefig(FIG_DIR / '02_kompaktlik_isitma.png', dpi=150); plt.show()"""),
md("**Yorum:** Yüksek (7.0) binalar sistematik olarak daha yüksek ısıtma yüküne sahiptir. Aynı yükseklikteki binalar arasında da kompaktlık arttıkça yük artmaktadır. İlişki tam doğrusal değildir; bu durum doğrusal modelin sınırlarından biri olacaktır."),
md("### 5.5 Grafik 3 — Cam alanına göre ortalama ısıtma yükü"),
code("""fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(by_glazing.index.astype(str), by_glazing['mean'], color='#3B8E5A')
for i, v in enumerate(by_glazing['mean']):
    ax.text(i, v + 0.3, f'{v:.1f}', ha='center')
ax.set_title('Cam alanı oranına göre ortalama ısıtma yükü')
ax.set_xlabel('Cam alanı oranı (glazing_area)'); ax.set_ylabel('Ortalama ısıtma yükü')
fig.tight_layout(); fig.savefig(FIG_DIR / '03_cam_alani_ortalama.png', dpi=150); plt.show()"""),
md("### 5.6 Grafik 4 — Özelliklerin hedefle korelasyonu"),
code("""features = list(COLUMNS.values())[:8]
corr = df[features + ['heating_load']].corr()['heating_load'].drop('heating_load').sort_values()
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(corr.index, corr.values, color=['#C73E1D' if v < 0 else '#2E86AB' for v in corr.values])
ax.set_title('Özelliklerin ısıtma yüküyle Pearson korelasyonu'); ax.set_xlabel('Korelasyon katsayısı')
ax.axvline(0, color='black', linewidth=0.8)
fig.tight_layout(); fig.savefig(FIG_DIR / '04_korelasyon.png', dpi=150); plt.show()
print(corr.round(3))"""),
md("### 5.7 Keşif bulguları\nBulgular aşağıdaki hücrede doğrudan veriden hesaplanır."),
code("""h = df.groupby('overall_height')['heating_load'].mean()
g = df.groupby('glazing_area')['heating_load'].mean()
o = df.groupby('orientation')['heating_load'].mean()
findings = {
    'yukseklik_ortalama_3_5': round(float(h.loc[3.5]), 2),
    'yukseklik_ortalama_7_0': round(float(h.loc[7.0]), 2),
    'cam_0_ortalama': round(float(g.loc[0.0]), 2),
    'cam_0_40_ortalama': round(float(g.loc[0.4]), 2),
    'yon_ortalama_fark': round(float(o.max() - o.min()), 3),
    'en_guclu_pozitif_korelasyon': [corr.idxmax(), round(float(corr.max()), 3)],
    'en_guclu_negatif_korelasyon': [corr.idxmin(), round(float(corr.min()), 3)],
}
print(f"1) Yükseklik belirleyici: 3.5 m binalarda ortalama {findings['yukseklik_ortalama_3_5']}, 7.0 m binalarda {findings['yukseklik_ortalama_7_0']}.")
print(f"2) Cam alanı arttıkça yük artıyor: cam yokken ortalama {findings['cam_0_ortalama']}, 0.40 oranında {findings['cam_0_40_ortalama']}.")
print(f"3) Yönün etkisi çok küçük: yönlere göre ortalamalar arasındaki en büyük fark {findings['yon_ortalama_fark']}.")
print(f"4) En güçlü pozitif ilişki: {findings['en_guclu_pozitif_korelasyon'][0]} (r = {findings['en_guclu_pozitif_korelasyon'][1]}); "
      f"en güçlü negatif ilişki: {findings['en_guclu_negatif_korelasyon'][0]} (r = {findings['en_guclu_negatif_korelasyon'][1]}).")"""),
md("""## 6. Model kurma ve eğitme

**Model seçim gerekçesi:** Hedef sayısal olduğu için regresyon gerekir. `LinearRegression` yorumlanabilir, hızlı ve eğitimdeki yöntemle uyumlu bir başlangıç modelidir. Her özelliğin tahmine etkisi bir katsayıyla görülebilir.

- `cooling_load`, ısıtma yüküyle birlikte simülasyonun bir çıktısıdır. Girdi olarak kullanılırsa hedef sızıntısı olur; bu yüzden modele alınmaz.
- Doğrusal regresyonun tahminleri özellik ölçeğinden etkilenmez; bu nedenle ölçeklendirme uygulanmadı. Böylece test verisinden bilgi sızması riski de oluşmaz."""),
code("""X = df[features]
y = df['heating_load']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('X_train:', X_train.shape, ' X_test:', X_test.shape, ' y_train:', y_train.shape, ' y_test:', y_test.shape)
print('Eğitim ve test indeksleri kesişiyor mu?', bool(set(X_train.index) & set(X_test.index)))
model = LinearRegression()
model.fit(X_train, y_train)
print('Model eğitildi.')"""),
md("## 7. Tahmin ve değerlendirme\nMAE, RMSE ve R² metrikleri eğitim ve test kümelerinde ayrı ayrı hesaplanır. `model.score` R² değerini verir."),
code("""def metrics(y_true, y_pred):
    return {'MAE': float(mean_absolute_error(y_true, y_pred)),
            'RMSE': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'R2': float(r2_score(y_true, y_pred))}

pred_train, pred_test = model.predict(X_train), model.predict(X_test)
results = pd.DataFrame({'Eğitim': metrics(y_train, pred_train), 'Test': metrics(y_test, pred_test)})
print(results.round(4))
print(f"\\nmodel.score(X_test, y_test) = {model.score(X_test, y_test):.4f}")
coef = pd.Series(model.coef_, index=features)
print('\\nKatsayılar:'); print(coef.round(4)); print('Sabit terim:', round(float(model.intercept_), 4))"""),
md("### Grafik 5 — Gerçek ve tahmin edilen değerler (test kümesi)"),
code("""fig, ax = plt.subplots(figsize=(5.5, 5))
ax.scatter(y_test, pred_test, s=16, alpha=0.7, color='#2E86AB')
lims = [min(y_test.min(), pred_test.min()) - 1, max(y_test.max(), pred_test.max()) + 1]
ax.plot(lims, lims, 'k--', linewidth=1, label='Mükemmel tahmin (y = x)')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_title('Test kümesi: gerçek ve tahmin edilen ısıtma yükü')
ax.set_xlabel('Gerçek ısıtma yükü'); ax.set_ylabel('Tahmin edilen ısıtma yükü'); ax.legend()
fig.tight_layout(); fig.savefig(FIG_DIR / '05_gercek_tahmin.png', dpi=150); plt.show()"""),
md("### Grafik 6 — Hata (artık) dağılımı"),
code("""residuals = y_test - pred_test
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(residuals, bins=25, color='#6C5B7B', edgecolor='white')
ax.axvline(0, color='black', linewidth=1)
ax.set_title('Test kümesi hata dağılımı (gerçek − tahmin)')
ax.set_xlabel('Hata'); ax.set_ylabel('Bina sayısı')
fig.tight_layout(); fig.savefig(FIG_DIR / '06_hata_dagilimi.png', dpi=150); plt.show()
err = pd.DataFrame({'gercek': y_test, 'tahmin': pred_test, 'abs_hata': residuals.abs(), 'yukseklik': X_test.overall_height})
print('Mutlak hata > 5 olan test örneği sayısı:', int((err.abs_hata > 5).sum()), '/', len(err))
print('Yüksekliğe göre ortalama mutlak hata:'); print(err.groupby('yukseklik')['abs_hata'].mean().round(3))
print('\\nEn büyük 5 hata:'); print(err.sort_values('abs_hata', ascending=False).head().round(2))"""),
md("""## 8. Yeni örnekler için tahmin

Üç yeni bina tanımlanır. Geometri değerleri (X1–X5) veri setindeki gerçek bina tiplerinden alınır. Bu değerler birbirine bağlıdır; rastgele bir kombinasyon fiziksel olarak tutarsız olabilir.

Cam alanı oranları (0.05, 0.15, 0.30) veri setinde **bulunmayan** ara değerlerdir. Bu nedenle bu girdiler modelin daha önce görmediği yeni örneklerdir."""),
code("""shapes = df[['relative_compactness', 'surface_area', 'wall_area', 'roof_area', 'overall_height']].drop_duplicates() \\
    .sort_values('relative_compactness', ascending=False).reset_index(drop=True)
new = pd.DataFrame([
    {**shapes.loc[0].to_dict(), 'orientation': 2, 'glazing_area': 0.05, 'glazing_area_distribution': 1},
    {**shapes.loc[5].to_dict(), 'orientation': 3, 'glazing_area': 0.15, 'glazing_area_distribution': 2},
    {**shapes.loc[11].to_dict(), 'orientation': 4, 'glazing_area': 0.30, 'glazing_area_distribution': 5},
])[features]
assert not new.merge(df[features], how='inner').shape[0], 'yeni örnekler veri setinde olmamalı'
new['tahmin_isitma_yuku'] = model.predict(new[features]).round(2)
new"""),
md("""## 9. Değerlendirme notu

- **Güvenilirlik:** Eğitim ve test metrikleri birbirine yakınsa aşırı öğrenme belirtisi yoktur; değerler yukarıdaki tabloda verilmiştir.
- **Sınırlar:** Doğrusal model, yükseklik ve kompaktlığın oluşturduğu doğrusal olmayan yapıyı ve iki kümeli dağılımı tam yakalayamaz. Bu durum hata grafiğinde görülür.
- **Katsayılar:** Geometri değişkenleri (X1–X4) birbirine bağlı olduğu için katsayılar tek tek "etki büyüklüğü" olarak yorumlanmamalıdır.
- **Veri:** Veri simülasyondan üretilmiştir ve yalnızca 12 bina şeklini kapsar. Gerçek binalara ve farklı iklimlere genelleme yapılamaz.
- **İyileştirme önerileri:**
  - Yön ve cam dağılım kodlarını one-hot kodlamak.
  - Etkileşim terimleri eklemek.
  - Karar ağacı veya rastgele orman gibi doğrusal olmayan modelleri denemek.
  - Çapraz doğrulama yapmak."""),
code("""summary = {'shape': list(df.shape), 'missing_total': int(df.isnull().sum().sum()),
           'n_train': int(len(X_train)), 'n_test': int(len(X_test)),
           'train_metrics': metrics(y_train, pred_train), 'test_metrics': metrics(y_test, pred_test),
           'model_score_test_R2': float(model.score(X_test, y_test)), 'findings': findings,
           'new_predictions': new['tahmin_isitma_yuku'].tolist()}
out = FIG_DIR.parent / 'notebook_metrics.json'
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print('Kaydedildi:', out)
print(json.dumps({k: summary[k] for k in ('n_train', 'n_test', 'test_metrics')}, indent=2))"""),
]

nb['cells'] = cells
nb['metadata'] = {'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
                  'language_info': {'name': 'python'}, 'colab': {'provenance': []},
                  'authors': [{'name': 'Tugay Sinan Ergün'}]}
out = ROOT / 'notebooks' / 'EnergyWise.ipynb'
nbf.write(nb, out)
print('written', out)
