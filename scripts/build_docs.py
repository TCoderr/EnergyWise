"""Generate docs/VERI_SOZLUGU.md (from the data) and reports/TEST_REPORT.md (from pytest's JUnit XML).
Run: .venv/Scripts/python scripts/build_docs.py
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import energywise_core as core  # noqa: E402

MEANING = {
    'relative_compactness': ('X1', 'Göreli kompaktlık: bina biçiminin ne kadar "toplu" olduğunu gösteren oran'),
    'surface_area': ('X2', 'Toplam dış yüzey alanı'),
    'wall_area': ('X3', 'Duvar alanı'),
    'roof_area': ('X4', 'Çatı alanı'),
    'overall_height': ('X5', 'Toplam bina yüksekliği'),
    'orientation': ('X6', 'Bina yönü (kod). UCI sayfası kodların anlamını vermiyor'),
    'glazing_area': ('X7', 'Cam alanı oranı'),
    'glazing_area_distribution': ('X8', 'Cam alanının cephelere dağılımı (kod). 0 yalnızca cam alanı 0 olduğunda görülür; diğer kodların anlamı UCI sayfasında verilmemiş'),
    'heating_load': ('Y1', '**Hedef (y):** ısıtma yükü'),
    'cooling_load': ('Y2', 'Soğutma yükü: ikinci hedef. Hedef sızıntısını önlemek için **girdi olarak kullanılmaz**'),
}
KIND = {'orientation': 'Sayısal kod (kategorik anlamlı)', 'glazing_area_distribution': 'Sayısal kod (kategorik anlamlı)'}


def data_dictionary():
    df = core.load_data()
    lines = ['# EnergyWise — Veri Sözlüğü', '',
             '**Kaynak:** UCI Machine Learning Repository — Energy Efficiency (Tsanas & Xifara, 2012), '
             'https://archive.ics.uci.edu/dataset/242/energy+efficiency · DOI 10.24432/C51307 · Lisans: CC BY 4.0',
             '',
             '**Dosyalar:**',
             '- `data/raw/energy_efficiency.zip`: resmî arşiv (`ENB2012_data.xlsx`).',
             '- `data/energy_efficiency.csv`: aynı değerler, okunur sütun adlarıyla (`src/energywise_core.py → build_csv_from_zip`).', '',
             f'**Boyut:** {df.shape[0]} satır × {df.shape[1]} sütun · **Eksik değer:** {int(df.isnull().sum().sum())} · '
             f'**Tekrarlanan satır:** {int(df.duplicated().sum())}', '',
             '> Veriler gerçek binalardan ölçülmemiştir. UCI açıklamasına göre değerler, Ecotect\'te simüle edilen 12 bina şeklinin enerji analizinden üretilmiştir. '
             'UCI sayfasında birim bilgisi verilmemiştir.', '',
             '| Sütun | UCI kodu | Rol | Tip | Pandas tipi | Min | Maks | Farklı değer | Anlamı |',
             '|---|---|---|---|---|---|---|---|---|']
    for c in df.columns:
        code, meaning = MEANING[c]
        role = 'Hedef (y)' if c == core.TARGET else ('Kullanılmıyor' if c == 'cooling_load' else 'Girdi (X)')
        lines.append(f'| `{c}` | {code} | {role} | {KIND.get(c, "Sayısal (sürekli)")} | {df[c].dtype} | '
                     f'{df[c].min():g} | {df[c].max():g} | {df[c].nunique()} | {meaning} |')
    lines += ['', '## Temizleme adımları', '',
              '1. Resmî xlsx dosyasındaki tamamen boş satırlar ve sütunlar atıldı (`dropna(how="all")`).',
              '2. Sütunlar X1–Y2 kodlarından okunur adlara çevrildi. **Değerler değiştirilmedi**; `tests/test_energywise.py::test_csv_matches_official_xlsx` bunu doğrular.',
              f'3. Eksik değer ({int(df.isnull().sum().sum())}) ve tekrarlanan satır ({int(df.duplicated().sum())}) bulunmadığı için doldurma veya silme yapılmadı.',
              '4. Veriden doğrulanan kural: cam alanı 0 ise cam dağılım kodu da 0\'dır. Konsol uygulaması bu kuralı uygular.']
    out = ROOT / 'docs' / 'VERI_SOZLUGU.md'; out.write_text('\n'.join(lines) + '\n', encoding='utf-8'); return out


def test_report():
    root = ET.parse(ROOT / 'reports' / 'test_results.xml').getroot()
    suite = root if root.tag == 'testsuite' else root.find('testsuite')
    total, fail, err, skip = (int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped'))
    meta = json.loads(core.META_PATH.read_text(encoding='utf-8'))
    lines = ['# EnergyWise — Test Raporu', '',
             f'**Tarih:** {suite.get("timestamp", "")[:19].replace("T", " ")} · **Ortam:** Python 3.12, scikit-learn {meta["sklearn_version"]} · '
             '**Komut:** `python -m pytest -v --junitxml=reports/test_results.xml`', '',
             f'**Sonuç:** {total} test · {total - fail - err - skip} başarılı · {fail} başarısız · {err} hata · {skip} atlandı · süre {float(suite.get("time", 0)):.2f} sn', '',
             '| # | Test | Sonuç | Süre (sn) |', '|---|---|---|---|']
    for i, tc in enumerate(suite.iter('testcase'), 1):
        status = 'BAŞARISIZ' if tc.find('failure') is not None else 'HATA' if tc.find('error') is not None else 'ATLANDI' if tc.find('skipped') is not None else 'BAŞARILI'
        lines.append(f'| {i} | `{tc.get("name")}` | {status} | {float(tc.get("time", 0)):.3f} |')
    lines += ['', '## Kapsam', '',
              '- **Veri:**',
              '  - 768×10 boyut ve sütun adları.',
              '  - Eksik değer yok.',
              '  - CSV ile resmî xlsx birebir aynı.',
              '  - 12 bina tipi var.',
              '  - cooling_load girdi değil.',
              '- **Model:**',
              '  - Bölme tekrarlanabilir ve kümeler ayrık (614 / 154).',
              '  - Kayıtlı metrikler yeniden eğitimle birebir aynı.',
              '  - Kalite alt sınırı (R² > 0,85) ve aşırı öğrenme kontrolü sağlanıyor.',
              '  - Değiştirilmiş model dosyası yüklenmiyor.',
              '- **tahmin_et():**',
              '  - Geçerli girdi.',
              '  - Hatalı girdiler (sayı olmayan, aralık dışı, izin verilmeyen kod) ve ardından doğru girdi.',
              '  - Cam alanı 0 kuralı.',
              '  - `q` ile çıkış.',
              '- **Uçtan uca:** `app.py` gerçek bir alt süreçte stdin ile çalıştırılıyor; menü, hata mesajı, tahmin ve çıkış doğrulanıyor.',
              '',
              '## Gerçek konsol çalıştırması', '',
              '`scripts/capture_console.py`, uygulamayı ayrı bir Windows konsol penceresinde (conhost + cmd) başlatır. '
              'Girdileri yalnızca o konsolun girdi tamponuna yazar (`WriteConsoleInputW`). '
              'Pencerenin görüntüsünü `PrintWindow` ile alır. Çıktılar:',
              '- `reports/console_screenshot.png`',
              '- `reports/console_transcript.txt`']
    out = ROOT / 'reports' / 'TEST_REPORT.md'; out.write_text('\n'.join(lines) + '\n', encoding='utf-8'); return out


if __name__ == '__main__':
    print(data_dictionary()); print(test_report())
