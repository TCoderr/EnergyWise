# Üç Proje — Final Kalite Denetimi ve Özet

**Author / Maintainer:** Tugay Sinan Ergün · **GitHub:** TCoderr · **Tarih:** 19 Ekim 2026 (TSİ)

Bu dosya, üç projenin geliştirmesi bittikten sonra yapılan bağımsız son denetimi özetler. Denetimde her projenin testleri ve teslim doğrulaması baştan çalıştırıldı. Ayrıntılı raporlar:

| Proje | Final rapor | Kontrol listesi | Doğrulama kayıtları |
|---|---|---|---|
| EnergyWise | `D:\Project\EnergyWise\FINAL_REPORT.md` | `D:\Project\EnergyWise\DELIVERY_CHECKLIST.md` | `EnergyWise\reports\delivery_verification.txt`, `zip_verification.txt` |
| PredictiveMaint AI | `D:\Project\PredictiveMaint-AI\FINAL_REPORT.md` | `D:\Project\PredictiveMaint-AI\DELIVERY_CHECKLIST.md` | `PredictiveMaint-AI\reports\delivery_verification.txt`, `zip_verification.txt`, `reproducibility_check.txt` |
| SchemaForge | `D:\Project\SchemaForge\FINAL_REPORT.md` | `D:\Project\SchemaForge\DELIVERY_CHECKLIST.md` | `SchemaForge\docs\TEST_REPORT.md`, `docs\test-results\*` |

## 1. Karşılaştırmalı tablo

| | EnergyWise | PredictiveMaint AI | SchemaForge |
|---|---|---|---|
| **Eğitim** | Yapay Zeka İçin Basitleştirilmiş Python | Makine ve Derin Öğrenme Uygulamaları | Web Geliştirme; Yapay Zeka |
| **Yönerge** | Yerelde bulundu (`OneDrive\Desktop\Proje\Basitleştirilmiş_Python_Proje_Envanteri.2026.docx`) | Yerelde bulundu (`…\Makine ve Derin Öğrenme Uygulamaları Proje Yönergesi.2026.docx`) | Yerelde bulundu (`…\Web Geliştirme; Yapay Zeka Proje Yönergesi.2026.docx`) |
| **Tamamlanan özellikler** | EDA (6 grafik, 4 bulgu); LinearRegression; MAE/RMSE/R²; 3 yeni tahmin; `tahmin_et()` konsol uygulaması; güvenli model yükleme; Colab uyumlu notebook | Sızıntısız ön işleme; 4 model; doğrulamayla model ve eşik seçimi; FN analizi; açıklanabilirlik; hata analizi; 9 görsel | Form CRUD + kopyalama; 7 alan türü; kurallar; canlı önizleme; LocalStorage + bozuk veri kurtarma; JSON dışa aktarma; responsive arayüz; erişilebilirlik |
| **Gerçek test sonuçları** | pytest 14/14 · notebook 19/19 hücre, 0 hata · teslim doğrulaması 16/16 | pytest 11/11 · notebook 19/19 hücre, 0 hata · yeniden çalıştırmada aynı sonuç · doğrulama 13/13 | tsc ✓ · ESLint ✓ · Vitest 33/33 · build ✓ · Playwright (Edge) yerel 4/4 + **canlı site 4/4** · doğrulama 15/15 |
| **Temel sonuç** | Test R² 0,9122 · MAE 2,182 | Random Forest, eşik 0,23: recall 0,853 · precision 0,879 · FN 10/68 | 12 kullanıcı senaryosunun hepsi otomatik testle geçti |
| **Başarısız kontroller** | Yok | Yok | Yok |
| **Eksik veya yapılmamış** | Colab'da çalıştırılmadı | Colab'da çalıştırılmadı | Otomatik kontrast denetimi yok · Netlify sitesi GitHub'a bağlı değil (sürekli dağıtım yok) |
| **Veri kaynağı** | UCI Energy Efficiency, CC BY 4.0, DOI 10.24432/C51307 (simülasyon verisi) | UCI AI4I 2020, CC BY 4.0, DOI 10.24432/C5HS5C (sentetik veri) | Harici veri yok |
| **Kurulan bağımlılıklar** | `.venv` (Py 3.12): pandas, numpy, scikit-learn, matplotlib, joblib, openpyxl + pytest, nbclient, ipykernel, python-docx, python-pptx, pypdf | `.venv` (Py 3.12): pandas, numpy, scikit-learn, matplotlib + pytest, nbclient, ipykernel, python-docx, pypdf | `node_modules`: react 19, typescript 6.0.3, vite 8, tailwindcss 4, vitest 5, testing-library, eslint 10, @playwright/test (kurulu Edge kullanıldı, tarayıcı indirilmedi) |
| **Teslim paketi** | `EnergyWise\dist\EnergyWise_Teslim.zip` | `PredictiveMaint-AI\dist\PredictiveMaint_AI_Teslim.zip` | `SchemaForge\release\SchemaForge_Teslim.zip` |
| **Bağlantılar (doğrulandı, HTTP 200)** | https://github.com/TCoderr/EnergyWise | https://github.com/TCoderr/PredictiveMaint-AI (rapora eklendi) | https://github.com/TCoderr/SchemaForge · canlı: https://schemaforge-tcoderr.netlify.app |
| **Kullanıcı işlemi** | Colab'da bir kez çalıştırma; bağlantıyı teslim formuna yazma | Colab'da bir kez çalıştırma; bağlantıyı teslim formuna yazma | GitHub ve Netlify bağlantılarını teslim formuna yazma; isteğe bağlı sürekli dağıtım |

## 2. Paket denetimi

- **İçerik:** Üç ZIP'te de CRC testi geçti. `.venv`, `node_modules`, `.git`, `.env` ve önbellek klasörü yok. Zorunlu dosyaların tamamı içeride (ilgili `zip_verification.txt`).
- **Dosyaların açılabilirliği:**
  - Notebook'lar nbformat ile okundu ve çalıştırıldı.
  - PDF'ler pypdf ile açıldı; sayfa sayısı ve metin kontrol edildi.
  - DOCX ve PPTX dosyaları Microsoft Word ve PowerPoint'te açılıp PDF'e aktarıldı.
- **Kök dizin:** `D:\Project` içinde yalnızca dört proje klasörü var; rastgele çıktı dosyası bırakılmadı.

## 3. Bilinmesi gerekenler

- **FormPilot-AI'a dokunulmadı.** Bu görev süresince klasörde değişen dosya yok; en son değişiklik saat 01:48'de.
- **FormPilot yönergesi bulundu:** `OneDrive\Desktop\Proje\Yapay Zeka ile İçerik Üretimi Proje Yönergesi.pdf`. FormPilot teslim raporunda "yönerge bulunamadı" yazıyor; o arama yalnızca `D:\Project` altını kapsamıştı. Bu, FormPilot raporunda sonradan düzeltilmesi gereken bir bilgi.
- **Dış hesap işlemleri (açık onayınla yapıldı):**
  - **GitHub:** Üç public depo `gh repo create` ile oluşturulup gönderildi. Ad çakışması önceden kontrol edildi. Gönderilen dosyalar gizli bilgi ve büyük dosya için tarandı. Uzak commit'lerin yereldekilerle aynı olduğu doğrulandı.
  - **Netlify:** Sen `netlify login` ile giriş yaptıktan sonra SchemaForge `tcoderr` ekibinde ücretsiz planla yayımlandı.
  - **Erişim ayarı:** Ekibin varsayılan "ziyaretçi erişimi: Netlify girişi" koruması, ikinci onayınla **yalnızca** `schemaforge-tcoderr` sitesi için kapatıldı. Ekip varsayılanı değişmedi (doğrulandı).
  - **Git kimliği:** Değiştirilmedi; commit'ler mevcut `TCoderr` kimliğiyle atıldı.
- **Ücretli hizmet kullanılmadı.** CUDA veya PyTorch kurulmadı.
- **Yazar alanları:** Bütün belgelerde yazar ve proje sahibi Tugay Sinan Ergün. Claude Code yalnızca kullanılan geliştirme aracı olarak anıldı.
