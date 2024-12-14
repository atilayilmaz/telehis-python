## Description (English)
As of December 14, 2024, the new project team for the 2024-2025 academic year has implemented the following changes to the existing codebase. The code is functional and successfully retrieves data, which is then uploaded to the AWS system as intended. However, there are still several deficiencies in the code. Development efforts to address these deficiencies are ongoing in the `develop` branch and specific `feature` branches.

## [v1.1.0] - 2024-12-14

### Added
- **New Files**:
  - `.gitignore`: Specifies files and directories to be ignored by Git.
  - `MovementMap.py`: Added functionality to handle movement mappings.
  - `awskey.pem`: Added the key file for AWS connection.
  - `data/`: New directory structure for input and output data.
    - `data/input/`: Includes example movement files (`movement_1.csv`, `movement_2.csv`, `movement_3.csv`).
    - `data/output/`: Directory for saving output files.
  - `requirements.txt`: Specifies Python dependencies.

### Changed
- **Hareket1_mediapipe.py**:
  - Integrated the `MovementMap` module.
  - Output file paths updated: all outputs are now saved under `data/output/`.
  - AWS key file path updated to `awskey.pem`.
  - Hardcoded file paths replaced with dynamic paths.
  - The `dtw` calculation process now uses `MovementMap` for dynamic file selection.

- **dtw.py**:
  - Output files are now saved under the `data/output/` directory.
  - Improved readability by simplifying missing data handling methods.

- **network_tools.py**:
  - Example usage of `sse_clients` function commented out for clarity.

- **Guide3.py**:
  - Renamed to `main.py` to better represent its role as the main executable file.

### Removed
- **None**: No files were removed in this version.

---

## Açıklama (Türkçe)
14 Aralık 2024 itibarıyla, 2024-2025 dönemi proje ekibi, mevcut kod üzerinde aşağıdaki değişiklikleri uygulamıştır. Kod çalışmaktadır ve verileri istenilen şekilde alıp AWS sistemine yüklemektedir. Ancak kodda halen birçok eksiklik bulunmaktadır. Bu eksiklikleri gidermek üzere çalışmalar `develop` branch'i ve belirli `feature` branch'lerinde devam etmektedir.

## [v1.1.0] - 2024-12-14

### Eklendi
- **Yeni Dosyalar**:
  - `.gitignore`: Git tarafından izlenmeyecek dosya ve dizinleri belirler.
  - `MovementMap.py`: Hareket haritalarını işlemek için işlevsellik eklendi.
  - `awskey.pem`: AWS bağlantısı için anahtar dosyası eklendi.
  - `data/`: Girdi ve çıktı verileri için yeni bir dizin yapısı.
    - `data/input/`: Örnek hareket dosyalarını içerir (`movement_1.csv`, `movement_2.csv`, `movement_3.csv`).
    - `data/output/`: Çıktı dosyalarının kaydedileceği dizin.
  - `requirements.txt`: Python bağımlılıklarını belirtir.

### Değiştirildi
- **Hareket1_mediapipe.py**:
  - `MovementMap` modülü entegre edildi.
  - Çıktı dosyalarının yolları güncellendi: tüm çıktılar artık `data/output/` altında kaydediliyor.
  - AWS anahtar dosyası yolu `awskey.pem` olarak değiştirildi.
  - Sabit kodlanmış dosya yolları dinamik hale getirildi.
  - `dtw` hesaplama süreci, dinamik dosya seçimi için `MovementMap` kullanımını içeriyor.

- **dtw.py**:
  - Çıktı dosyaları artık `data/output/` dizininde kaydediliyor.
  - Eksik veri doldurma yöntemleri basitleştirilerek okunabilirlik artırıldı.

- **network_tools.py**:
  - `sse_clients` fonksiyonunun örnek kullanımı netlik için yorum satırı haline getirildi.

- **Guide3.py**:
  - Ana yürütülebilir dosya rolünü daha iyi temsil etmek için `main.py` olarak yeniden adlandırıldı.

### Kaldırıldı
- **Hiçbiri**: Bu versiyonda herhangi bir dosya kaldırılmadı.
