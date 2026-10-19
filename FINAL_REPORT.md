# EnergyWise — Final Raporu

**Author / Maintainer:** Tugay Sinan Ergün · **GitHub:** TCoderr · **Tarih:** 19 Ekim 2026
**Eğitim:** Yapay Zeka İçin Basitleştirilmiş Python

## 1. Sonuç

Proje uçtan uca tamamlandı:
- **Notebook:** Gerçek UCI verisiyle yerelde baştan sona hatasız çalıştı (19 kod hücresi).
- **Model ve konsol uygulaması:** Model eğitildi; konsol uygulaması gerçek bir Windows konsolunda çalıştırıldı.
- **Testler:** 14 otomatik testin tamamı geçti.
- **Rapor ve sunum:** Rapor (1 sayfa) ve sunum (5 slayt) gerçek çıktılardan üretildi ve Microsoft Office'te açılarak PDF'e aktarıldı.

**GitHub:** https://github.com/TCoderr/EnergyWise (public). Proje sahibinin onayıyla oluşturuldu ve doğrulandı.

**Tek açık konu:** Notebook Google Colab'da çalıştırılmadı (erişim yok).

## 2. Model sonuçları

| Metrik | Eğitim (614) | Test (154) |
|---|---|---|
| MAE | 2,041 | 2,182 |
| RMSE | 2,893 | 3,025 |
| R² | 0,9171 | 0,9122 |

- **Değerlendirme:** Eğitim ve test sonuçları birbirine yakın; belirgin aşırı öğrenme yok.
- **Zayıf yön:** Doğrusal model, yüksekliğe bağlı iki kümeli yapıyı tam yakalayamıyor. Hata dağılımının uçlarında ayrı kümeler görülüyor.
- **Yeni tahminler:** Veri setinde bulunmayan 3 bina için tahminler: 23,84 · 34,82 · 17,21.

## 3. Veri

- **Kaynak:** UCI Energy Efficiency (Tsanas & Xifara, 2012), CC BY 4.0, DOI 10.24432/C51307.
- **İndirme:** `https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip`, 19.10.2026.
- **Arşiv SHA-256:** `499441ee…6738351`
- **Boyut:** 768 satır, 10 sütun, eksik değer yok.
- **Niteliği:** Ecotect simülasyon verisidir, gerçek ölçüm değildir.
- **Belirtilmeyen bilgiler:** UCI sayfasında birim ile yön ve cam dağılım kodlarının anlamı verilmemiştir; bu bilgiler yorumlanmadı.
- **Kullanılmayan sütun:** `cooling_load` hedef sızıntısını önlemek için kullanılmadı.

## 4. Doğrulama

| Kontrol | Sonuç | Kanıt |
|---|---|---|
| Otomatik testler | 14/14 başarılı | `reports/TEST_REPORT.md`, `reports/test_results.xml` |
| Notebook çalıştırma | 19/19 hücre, 0 hata | `notebooks/EnergyWise.ipynb` (çıktılarıyla) |
| Sayı tutarlılığı | Notebook = model metadata = rapor = sunum = README | `reports/delivery_verification.txt` |
| Office'te açılma | Rapor 1 sayfa (Word), sunum 5 slayt (PowerPoint) | `reports/office_open_check.json` |
| Gerçek konsol | conhost penceresinde çalıştırma, ekran görüntüsü ve metin kaydı | `reports/console_screenshot.png`, `reports/console_transcript.txt` |
| ZIP | CRC testi; `.venv`/önbellek/`.env` yok; zorunlu dosyalar var | `reports/zip_verification.txt` |

**Çalışma sırasında bulunup düzeltilen sorunlar:**
- İlk konsol çekiminde `app.py` başlamadı; Python'un `Popen` tırnak kaçışı cmd'yi bozuyordu. Başlatıcı `.cmd` dosyasıyla düzeltildi.
- Ekran görüntüsü DPI ölçeklemesi nedeniyle kırpılıyordu. DPI farkındalığı eklendi.
- Sunumda iki görsel slayt dışına taşıyordu; yerleşim düzeltildi.
- Doğrulama script'i `https://` ifadesini Windows yolu sandı; regex düzeltildi.

## 5. Kurulan bağımlılıklar

Proje içi `.venv` (Python 3.12.10):
- **Çalışma için:** pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, matplotlib 3.11.2, joblib 1.6.0, openpyxl 3.1.5.
- **Test ve belge üretimi için:** pytest 9.1.1, nbformat 5.11.1, nbclient 0.11.0, ipykernel 7.4.0, python-docx 1.2.0, python-pptx 1.0.2, pypdf 6.21.1.

Ücretli hizmet kullanılmadı. PDF dışa aktarma yerel Microsoft Office ile yapıldı.

## 6. Teslim paketi

`D:\Project\EnergyWise\dist\EnergyWise_Teslim.zip`

## 7. Kullanıcı aksiyonları

1. Notebook'u Google Colab'da bir kez çalıştır.
2. Teslim formu bağlantı istiyorsa GitHub adresini kullan: https://github.com/TCoderr/EnergyWise

## 8. Araçlar ve kaynaklandırma

Kod ve belgeler Claude Code (Anthropic) yardımıyla geliştirildi ve test edildi. Proje sahibi ve sorumlusu Tugay Sinan Ergün'dür.
