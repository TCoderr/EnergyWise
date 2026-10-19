# EnergyWise — Teslim Kontrol Listesi

**Proje:** EnergyWise — Bina Isıtma Yükü Tahmini · **Eğitim:** Yapay Zeka İçin Basitleştirilmiş Python
**Author / Maintainer:** Tugay Sinan Ergün · **GitHub:** TCoderr · **Tarih:** 19 Ekim 2026

**Yönerge:** `Basitleştirilmiş_Python_Proje_Envanteri.2026.docx` (yerelde bulundu ve esas alındı)

Durum: ✅ tamamlandı ve doğrulandı · ⚠️ tamamlandı, açık not var · 👤 kullanıcı yapacak

## Yönerge aşamaları

| Aşama | Gereksinim | Dosya | Kanıt | Durum |
|---|---|---|---|---|
| 1 | Proje tanım formu (problem cümlesi, hedef, tür) + gerekçe | `notebooks/EnergyWise.ipynb` §1, rapor §1 | — | ✅ |
| 2 | CSV veri (≥20 satır, ≥2 özellik), `pd.read_csv` | `data/energy_efficiency.csv` | 768 satır, 8 girdi; test: CSV = resmî xlsx | ✅ |
| 2 | Veri sözlüğü (ad, tip, anlam) | `docs/VERI_SOZLUGU.md` | veriden üretildi | ✅ |
| 2 | Eksik/hatalı değer kontrolü ve temizleme açıklaması | notebook §3–4, veri sözlüğü | eksik 0, tekrar 0 | ✅ |
| 3 | `head`, `shape`, `describe`, `groupby`, `value_counts` | notebook §3, §5 | doğrulama scripti kontrol ediyor | ✅ |
| 3 | En az 2 etiketli grafik + yorum | `reports/figures/01–06_*.png` | 6 grafik, hepsinde başlık ve eksen etiketi | ✅ |
| 3 | 3–5 keşif bulgusu | notebook §5.7, rapor §3 | 4 bulgu, veriden hesaplandı | ✅ |
| 4 | X/y ayırma, `train_test_split`, model seçimi, `fit` | notebook §6 | random_state=42; 614/154; kümeler ayrık (test) | ✅ |
| 4 | Model seçim gerekçesi ve bölünme boyutları | notebook §6 | — | ✅ |
| 5 | `predict` ve başarı ölçümü | notebook §7 | MAE 2,182 · RMSE 3,025 · R² (`model.score`) 0,9122 | ✅ |
| 5 | En az 3 yeni örnek tahmini | notebook §8, rapor §5 | 23,84 · 34,82 · 17,21 (veri setinde olmayan girdiler) | ✅ |
| 5 | Değerlendirme notu (güvenilirlik, aşırı öğrenme, zayıf yönler) | notebook §9, rapor §5 | eğitim R² 0,9171 / test 0,9122 | ✅ |
| 6 | `tahmin_et()` + `input()` + f-string | `app.py` | 4 birim testi + uçtan uca alt süreç testi | ✅ |
| 6 | Örnek çalıştırma ekran görüntüsü | `reports/console_screenshot.png`, `reports/console_transcript.txt` | gerçek conhost penceresi | ✅ |
| 7 | 3–5 slayt sunum + en önemli grafik | `presentation/EnergyWise_Sunum.pptx` + `.pdf` | 5 slayt, PowerPoint'te açıldı | ✅ |
| 7 | 1 sayfalık rapor | `reports/EnergyWise_Proje_Raporu.pdf` (+ `.docx`) | Word'de 1 sayfa | ✅ |
| 7 | Düzenli, yorumlu Colab not defteri | `notebooks/EnergyWise.ipynb` | yerelde hatasız çalıştı; Windows yolu yok | ⚠️ Colab'da çalıştırılmadı |

## Ek gereksinimler

| Gereksinim | Dosya / kanıt | Durum |
|---|---|---|
| Resmî kaynaktan veri, kaynaklandırma | `data/raw/energy_efficiency.zip` (UCI, SHA-256 kayıtlı), README | ✅ |
| Simülasyon verisi olduğunun açıkça belirtilmesi | README, notebook, rapor, sunum, veri sözlüğü | ✅ |
| MAE, RMSE, R²; eğitim/test karşılaştırması; hata dağılımı; gerçek–tahmin grafiği | notebook §7, grafik 05–06 | ✅ |
| Girdi doğrulama, açıklayıcı hata mesajları, çıkış seçeneği | `app.py`, testler | ✅ |
| Model güvenli yükleme | SHA-256 + scikit-learn sürüm kontrolü; değiştirilmiş model reddediliyor (test) | ✅ |
| `requirements.txt` | `requirements.txt` (çalışma), `requirements-dev.txt` (test/rapor) | ✅ |
| README + Colab talimatı | `README.md` | ✅ |
| Test raporu | `reports/TEST_REPORT.md`, `reports/test_results.xml` (14/14) | ✅ |
| Teslim doğrulaması | `reports/delivery_verification.txt`, `reports/zip_verification.txt` | ✅ |
| ZIP paketi | `dist/EnergyWise_Teslim.zip` | ✅ |

## Kullanıcı aksiyonları

1. 👤 Notebook'u Google Colab'da bir kez "Tümünü çalıştır" ile doğrula (README → Google Colab).
2. 👤 Eğitimin teslim formu GitHub veya Colab bağlantısı istiyorsa paylaşım bağlantısını kendi hesabından oluştur. Bu projede GitHub'a gönderim yapılmadı.
