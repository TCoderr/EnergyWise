# EnergyWise — Veri Sözlüğü

**Kaynak:** UCI Machine Learning Repository — Energy Efficiency (Tsanas & Xifara, 2012), https://archive.ics.uci.edu/dataset/242/energy+efficiency · DOI 10.24432/C51307 · Lisans: CC BY 4.0

**Dosyalar:**
- `data/raw/energy_efficiency.zip`: resmî arşiv (`ENB2012_data.xlsx`).
- `data/energy_efficiency.csv`: aynı değerler, okunur sütun adlarıyla (`src/energywise_core.py → build_csv_from_zip`).

**Boyut:** 768 satır × 10 sütun · **Eksik değer:** 0 · **Tekrarlanan satır:** 0

> Veriler gerçek binalardan ölçülmemiştir. UCI açıklamasına göre değerler, Ecotect'te simüle edilen 12 bina şeklinin enerji analizinden üretilmiştir. UCI sayfasında birim bilgisi verilmemiştir.

| Sütun | UCI kodu | Rol | Tip | Pandas tipi | Min | Maks | Farklı değer | Anlamı |
|---|---|---|---|---|---|---|---|---|
| `relative_compactness` | X1 | Girdi (X) | Sayısal (sürekli) | float64 | 0.62 | 0.98 | 12 | Göreli kompaktlık: bina biçiminin ne kadar "toplu" olduğunu gösteren oran |
| `surface_area` | X2 | Girdi (X) | Sayısal (sürekli) | float64 | 514.5 | 808.5 | 12 | Toplam dış yüzey alanı |
| `wall_area` | X3 | Girdi (X) | Sayısal (sürekli) | float64 | 245 | 416.5 | 7 | Duvar alanı |
| `roof_area` | X4 | Girdi (X) | Sayısal (sürekli) | float64 | 110.25 | 220.5 | 4 | Çatı alanı |
| `overall_height` | X5 | Girdi (X) | Sayısal (sürekli) | float64 | 3.5 | 7 | 2 | Toplam bina yüksekliği |
| `orientation` | X6 | Girdi (X) | Sayısal kod (kategorik anlamlı) | int64 | 2 | 5 | 4 | Bina yönü (kod). UCI sayfası kodların anlamını vermiyor |
| `glazing_area` | X7 | Girdi (X) | Sayısal (sürekli) | float64 | 0 | 0.4 | 4 | Cam alanı oranı |
| `glazing_area_distribution` | X8 | Girdi (X) | Sayısal kod (kategorik anlamlı) | int64 | 0 | 5 | 6 | Cam alanının cephelere dağılımı (kod). 0 yalnızca cam alanı 0 olduğunda görülür; diğer kodların anlamı UCI sayfasında verilmemiş |
| `heating_load` | Y1 | Hedef (y) | Sayısal (sürekli) | float64 | 6.01 | 43.1 | 587 | **Hedef (y):** ısıtma yükü |
| `cooling_load` | Y2 | Kullanılmıyor | Sayısal (sürekli) | float64 | 10.9 | 48.03 | 636 | Soğutma yükü: ikinci hedef. Hedef sızıntısını önlemek için **girdi olarak kullanılmaz** |

## Temizleme adımları

1. Resmî xlsx dosyasındaki tamamen boş satırlar ve sütunlar atıldı (`dropna(how="all")`).
2. Sütunlar X1–Y2 kodlarından okunur adlara çevrildi. **Değerler değiştirilmedi**; `tests/test_energywise.py::test_csv_matches_official_xlsx` bunu doğrular.
3. Eksik değer (0) ve tekrarlanan satır (0) bulunmadığı için doldurma veya silme yapılmadı.
4. Veriden doğrulanan kural: cam alanı 0 ise cam dağılım kodu da 0'dır. Konsol uygulaması bu kuralı uygular.
