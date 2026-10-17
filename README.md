# Uzay Oyunu – Hafta 4 Lab (Üreteçler ve functools)

Öğrenci: Timuçin KAVAK _____  Numara: 20244029034_____

## Görev 4 – Önbellek ölçümü
Komut: `uv run python -m uzay_oyunu.akis` (dünya, adim=20)

| Sürüm | Süre |
| Önbelleksiz | 1.2046  sn () |
| `@lru_cache` ile | 0.000063 sn |

`cache_info()` çıktısı: `CacheInfo(hits=47, misses=50, maxsize=None, currsize=50)`

Yorum: Önbellek aynı (gezegen, adım) alt problemlerini tekrar hesaplamayı
engeller; önbelleksiz sürümde çağrı sayısı adımla üstel artar, önbelleklide
yalnızca farklı (gezegen, adım) çifti kadar hesap yapılır.
