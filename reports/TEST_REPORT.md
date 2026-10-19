# EnergyWise — Test Raporu

**Tarih:** 2026-10-19 02:36:55 · **Ortam:** Python 3.12, scikit-learn 1.9.1 · **Komut:** `python -m pytest -v --junitxml=reports/test_results.xml`

**Sonuç:** 14 test · 14 başarılı · 0 başarısız · 0 hata · 0 atlandı · süre 3.30 sn

| # | Test | Sonuç | Süre (sn) |
|---|---|---|---|
| 1 | `test_dataset_shape_and_columns` | BAŞARILI | 0.003 |
| 2 | `test_no_missing_values_and_numeric` | BAŞARILI | 0.001 |
| 3 | `test_csv_matches_official_xlsx` | BAŞARILI | 0.241 |
| 4 | `test_twelve_building_shapes` | BAŞARILI | 0.002 |
| 5 | `test_cooling_load_not_a_feature` | BAŞARILI | 0.000 |
| 6 | `test_split_is_reproducible_and_disjoint` | BAŞARILI | 0.003 |
| 7 | `test_saved_metadata_matches_fresh_training` | BAŞARILI | 0.045 |
| 8 | `test_model_quality_is_reasonable` | BAŞARILI | 0.000 |
| 9 | `test_tampered_model_is_refused` | BAŞARILI | 0.004 |
| 10 | `test_tahmin_et_valid_input` | BAŞARILI | 0.004 |
| 11 | `test_tahmin_et_rejects_bad_input_then_accepts` | BAŞARILI | 0.003 |
| 12 | `test_zero_glazing_forces_distribution_zero` | BAŞARILI | 0.003 |
| 13 | `test_q_exits` | BAŞARILI | 0.002 |
| 14 | `test_app_end_to_end_subprocess` | BAŞARILI | 1.576 |

## Kapsam

- **Veri:**
  - 768×10 boyut ve sütun adları.
  - Eksik değer yok.
  - CSV ile resmî xlsx birebir aynı.
  - 12 bina tipi var.
  - cooling_load girdi değil.
- **Model:**
  - Bölme tekrarlanabilir ve kümeler ayrık (614 / 154).
  - Kayıtlı metrikler yeniden eğitimle birebir aynı.
  - Kalite alt sınırı (R² > 0,85) ve aşırı öğrenme kontrolü sağlanıyor.
  - Değiştirilmiş model dosyası yüklenmiyor.
- **tahmin_et():**
  - Geçerli girdi.
  - Hatalı girdiler (sayı olmayan, aralık dışı, izin verilmeyen kod) ve ardından doğru girdi.
  - Cam alanı 0 kuralı.
  - `q` ile çıkış.
- **Uçtan uca:** `app.py` gerçek bir alt süreçte stdin ile çalıştırılıyor; menü, hata mesajı, tahmin ve çıkış doğrulanıyor.

## Gerçek konsol çalıştırması

`scripts/capture_console.py`, uygulamayı ayrı bir Windows konsol penceresinde (conhost + cmd) başlatır. Girdileri yalnızca o konsolun girdi tamponuna yazar (`WriteConsoleInputW`). Pencerenin görüntüsünü `PrintWindow` ile alır. Çıktılar:
- `reports/console_screenshot.png`
- `reports/console_transcript.txt`
