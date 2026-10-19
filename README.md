# EnergyWise — Bina Isıtma Yükü Tahmini

**Eğitim:** Yapay Zeka İçin Basitleştirilmiş Python — "Uçtan Uca Yapay Zeka Projesi: Veriden Tahmine"
**Author / Maintainer:** Tugay Sinan Ergün · **GitHub:** TCoderr

Bir binanın mimari özelliklerinden **ısıtma yükünü** tahmin eden Python projesi. İçinde:
- veri analizi (Pandas, NumPy, Matplotlib),
- `LinearRegression` modeli (scikit-learn),
- terminalden girdi alan bir tahmin uygulaması (`tahmin_et()`).

> **Veri hakkında:** UCI Energy Efficiency veri seti gerçek binalardan ölçülmemiştir. Değerler, Ecotect'te simüle edilen 12 bina şeklinin enerji analizinden üretilmiştir. Sonuçlar bu simülasyon koşulları için geçerlidir.

## Sonuçlar (test kümesi, 154 bina)

| Metrik | Eğitim (614) | Test (154) |
|---|---|---|
| MAE | 2,041 | 2,182 |
| RMSE | 2,893 | 3,025 |
| R² | 0,9171 | 0,9122 |

Ayrıntılar:
- Rapor: `reports/EnergyWise_Proje_Raporu.pdf`
- Notebook: `notebooks/EnergyWise.ipynb`
- Ham metrikler: `reports/notebook_metrics.json`, `models/model_metadata.json`

## Klasör yapısı

```
EnergyWise/
├── app.py                      # konsol uygulaması: tahmin_et()
├── src/energywise_core.py      # veri yükleme/doğrulama, eğitim, güvenli model yükleme
├── src/train_model.py          # CSV'yi resmî zip'ten üretir, modeli eğitir ve kaydeder
├── notebooks/EnergyWise.ipynb  # Colab uyumlu analiz + model notebook'u (çalıştırılmış çıktılarıyla)
├── data/raw/energy_efficiency.zip  # UCI resmî arşivi (ENB2012_data.xlsx)
├── data/energy_efficiency.csv      # kaynak veri CSV (değerler değiştirilmedi)
├── docs/VERI_SOZLUGU.md        # veri sözlüğü ve temizleme adımları
├── models/                     # eğitilmiş model + metadata (sha256, metrikler)
├── reports/                    # rapor (DOCX/PDF), grafikler, test raporu, konsol ekran görüntüsü
├── presentation/               # 5 slaytlık sunum (PPTX/PDF)
├── tests/test_energywise.py    # 14 otomatik test
└── scripts/                    # notebook/rapor/sunum üretimi, Office dışa aktarma, doğrulama, paketleme
```

## Yerel kurulum (Windows, Python 3.12)

```powershell
cd EnergyWise
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt      # yalnızca uygulama ve notebook için
.venv\Scripts\python src\train_model.py                       # modeli yeniden üretir (isteğe bağlı)
.venv\Scripts\python app.py                                   # konsol uygulaması
```

Testler ve rapor üretimi için ayrıca: `.venv\Scripts\python -m pip install -r requirements-dev.txt`, ardından `.venv\Scripts\python -m pytest -v`.

## Konsol uygulaması

`python app.py` komutu menüyü açar:
- `1`: tahmin yap
- `2`: 12 bina tipini göster
- `q`: çıkış (her soruda da çalışır)

`tahmin_et()` sırasıyla şunları sorar:
1. Bina tipi (1–12; veri setindeki geometriler).
2. Yön kodu (2–5).
3. Cam alanı oranı (0–0,40; virgül veya nokta).
4. Cam dağılım kodu (1–5). Cam alanı 0 ise bu kod otomatik olarak 0 alınır.

Hatalı girdilerde açıklayıcı bir mesaj gösterir ve soruyu tekrarlar. Sonucu f-string ile yazdırır.

Uygulama modeli yalnızca `models/model_metadata.json` içindeki SHA-256 değeri ve scikit-learn sürümü eşleşirse yükler. joblib/pickle dosyaları kod çalıştırabildiği için bilinmeyen veya değiştirilmiş bir model dosyası yüklenmez. Eşleşme yoksa `python src/train_model.py` ile model yeniden üretilir.

Gerçek çalıştırma kanıtı:
- Ekran görüntüsü: `reports/console_screenshot.png`
- Metin kaydı: `reports/console_transcript.txt`

## Bağlantılar

- **GitHub (public):** https://github.com/TCoderr/EnergyWise
- **Colab'da aç:** [notebooks/EnergyWise.ipynb](https://colab.research.google.com/github/TCoderr/EnergyWise/blob/main/notebooks/EnergyWise.ipynb). Bu, Colab'ın public GitHub notebook'larını açan resmî adres biçimidir.

## Google Colab'da çalıştırma

1. Yukarıdaki "Colab'da aç" bağlantısını kullan **veya** https://colab.research.google.com → **Dosya → Not defteri yükle** → `notebooks/EnergyWise.ipynb`.
2. **Çalışma zamanı → Tümünü çalıştır.** Notebook proje dosyalarını bulamazsa veriyi resmî UCI adresinden (`https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip`) indirir. Bunun için internet gerekir. Grafikler `figures/` klasörüne kaydedilir.
3. Gerekli kütüphaneler (pandas, numpy, matplotlib, scikit-learn, openpyxl) Colab'da hazır gelir; ek kurulum gerekmez.

> **Doğrulama durumu:** Notebook yerelde (Python 3.12, nbclient) baştan sona hatasız çalıştırıldı. **Google Colab'da çalıştırılmadı**; Colab'daki kütüphane sürümleri farklı olabilir. Teslimden önce yukarıdaki adımlarla bir kez Colab'da çalıştırın.

## Yeniden üretim (bütün çıktılar)

```powershell
.venv\Scripts\python src\train_model.py
.venv\Scripts\python scripts\build_notebook.py
.venv\Scripts\python -c "import nbformat; from nbclient import NotebookClient; nb=nbformat.read('notebooks/EnergyWise.ipynb',4); NotebookClient(nb, timeout=300, resources={'metadata':{'path':'.'}}).execute(); nbformat.write(nb,'notebooks/EnergyWise.ipynb')"
.venv\Scripts\python -m pytest -v --junitxml=reports/test_results.xml
.venv\Scripts\python scripts\capture_console.py        # gerçek konsol ekran görüntüsü (Windows)
.venv\Scripts\python scripts\build_report.py
powershell -ExecutionPolicy Bypass -File scripts\export_office.ps1   # PDF'ler (Microsoft Office gerekir)
.venv\Scripts\python scripts\build_docs.py
.venv\Scripts\python scripts\verify_delivery.py
.venv\Scripts\python scripts\package.py
```

## Veri kaynağı ve lisans

- **Veri:** Tsanas, A. & Xifara, A. (2012). *Energy Efficiency* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C51307. Lisans: **CC BY 4.0**.
- **Makale:** A. Tsanas, A. Xifara, "Accurate quantitative estimation of energy performance of residential buildings using statistical machine learning tools", *Energy and Buildings*, 49 (2012).
- **Geliştirme:** Kod, Claude Code (Anthropic) yardımıyla geliştirildi ve test edildi. Proje sahibi ve sorumlusu Tugay Sinan Ergün'dür.
