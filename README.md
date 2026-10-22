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

---

# Hafta 5 Lab – Dekoratörler

Dekoratörler `uzay_oyunu/dekoratorler.py`, komutlar `uzay_oyunu/komutlar.py` içinde.
Hepsi `functools.wraps` kullanır (ad/belge korunur) ve `tests/` altında test edilir.
Çalıştırma: `uv run pytest`

**Dekoratör nedir?** `@d` satırı, fonksiyon *tanımlanırken* bir kez çalışır ve fonksiyonun
yerine bir sarmalayıcı koyar (`f = d(f)`). Sarmalayıcının gövdesi ise fonksiyon her
*çağrıldığında* çalışır. Aşağıda her görevde "tanım anı / çağrı anı" ayrımı bu yüzden var.

## Görev 1 – Süre ölçen dekoratör (`sure_olc`)
- **Ne yaptık:** `time.perf_counter()` ile fonksiyonu ölçüp `ad: 0.0123 sn` yazdıran, sonucu
  aynen döndüren `sure_olc` yazdık. Hafta 4'ten kalma `araclar.sure_olc` (farklı çıktı biçimi)
  kaldırıldı; `araclar` artık bunu `dekoratorler`'den alıyor (tek yerde tanım).
- **Neden:** Ölçüm kodunu her fonksiyona kopyalamak yerine tek bir dekoratörle ekleriz.
  `*args/**kwargs` her imzayla çalışmasını, `return` sonucun değişmemesini, `wraps` ise
  `__name__`/`__doc__` korunmasını sağlar.
- **Uygulama:** `akis.olc_dekoratorlu` önbelleksiz rota sayacını sarmalar (adim=20):

```
rota_sayisi: 2.5882 sn
```
<!-- bu süre geliştirme ortamında ölçüldü; kendi makinende `uv run python -m uzay_oyunu.akis` ile ölçüp güncelle -->
- **Testler:** sonuç değişmeden dönüyor, adlı argümanlarla çağrı çalışıyor, `__name__`/`__doc__` korunuyor.

## Görev 2 – Çağrı sayacı ve dekoratör sırası (`say`)
- **Ne yaptık:** Çağrıları `sarmalayici.cagri` niteliğinde sayan `say` yazdık; `fib_sirasi.py`
  içinde özyinelemeli Fibonacci'yi üç biçimde tanımladık.
- **Neden:** Dekoratör sırasının sonucu nasıl değiştirdiğini görmek için.

| Biçim | `fib(20)` çağrı sayısı |
|---|---|
| Yalnızca `@say` | 21891 |
| `@say` üstte, `@lru_cache` altta | 39 |
| `@lru_cache` üstte, `@say` altta (`fib.__wrapped__.cagri`) | 21 |

Kısa özet: önbellek üstteyse sayaç yalnızca gerçek hesapları (miss) görür; sayaç üstteyse
önbellek isabetlerini de sayar. Ayrıntılı açıklama: [`dekorator_sirasi.md`](dekorator_sirasi.md).

## Görev 3 – Loglayan dekoratör (`log_cagri`)
- **Ne yaptık:** Çağrıdan önce ad ve argümanları (konumsal + adlı), sonra dönüş değerini
  yazdıran `log_cagri` yazdık; `galaksi_kur` ve `hedef_menusu`'ne uyguladık.
- **Neden:** Hata ayıklarken fonksiyonların neyle çağrıldığını ve ne döndürdüğünü kodu
  değiştirmeden görmek için.
- **Dikkat:** `hedef_menusu`'nün doctest'i log satırlarını da içerecek şekilde güncellendi; aksi
  halde doctest bozulurdu. Eski testler çalışmaya devam ediyor (değerler değişmiyor, yalnızca
  ekrana ek yazı çıkıyor).

```
-> galaksi_kur(gezegenler=[...], baglantilar={...}, baslangic='dünya', yakit=100)
<- galaksi_kur = {'gezegenler': [...], ...}
-> hedef_menusu(['centauri', 'orion'])
<- hedef_menusu = 'Nereye gitmek istersin?\n[1] centauri\n[2] orion'
```

## Görev 4 – Komut sistemi: kayıt deseni (`komutlar.py`)
- **Ne yaptık:** `KOMUTLAR` sözlüğü ve argüman alan `komut(ad, aciklama="")` dekoratörü.
  Dekoratör fonksiyonu **değiştirmeden** `(fonksiyon, aciklama)` olarak kaydeder; aynı ad iki
  kez kullanılırsa tanım anında `ValueError` fırlatır. Üç komut: `yardim`, `envanter`, `harita`.
- **Neden:** Yeni komut eklemek `travel()` içine `if/elif` yazmak yerine yalnızca bir fonksiyon
  tanımlayıp `@komut(...)` eklemek olur (kayıt/registry deseni). Fonksiyonu sarmalamadığımız
  için komutlar doğrudan da çağrılıp test edilebilir.
- **`travel()` entegrasyonu:** girdi bir komut adıysa komut, `{konum, baglantilar, credits,
  engines, copilot}` durum sözlüğüyle çalıştırılır, sonuç yazdırılır ve `continue` ile aynı menü
  tekrar gösterilir (hamle/yakıt harcanmaz). Komut değilse eskisi gibi gezegen seçimi sayılır.

```
Nereye gitmek istersin?
[1] centauri
[2] orion
> yardim
envanter  eşyalarını gösterir
harita    gidebileceğin gezegenleri gösterir
yardim    komutları listeler
> harita
centauri, orion
```

## Görev 5 – Argüman alan dekoratör (`sinirla`)
- **Ne yaptık:** `sinirla(alt, ust)` ilk argüman `[alt, ust]` dışındaysa anlamlı `ValueError`
  fırlatır (sınırlar dahil). `oyun.yakit_harca(miktar)` fonksiyonuna `@sinirla(0, 100)` uyguladık.
- **Neden:** Doğrulama kodunu fonksiyon gövdesinden ayırır. Parametre alan dekoratör üç
  katmandır: `sinirla(alt, ust)` → `dekorator(f)` → `sarmalayici(*args, **kwargs)`.

```
>>> yakit_harca(30)
70
>>> yakit_harca(150)
ValueError: yakit_harca: 150 değeri 0-100 aralığında değil
```
- **Testler:** 0 ve 100 (sınır), 30 (normal), -1/101/150 (aralık dışı) ayrı ayrı denendi.

## Bonus – `hafiza(maxsize=None)`
- **Ne yaptık:** `lru_cache` kullanmadan, closure içindeki sözlükle çalışan önbellek. `maxsize`
  dolunca en eski (ilk eklenen) girdi silinir.
- **Neden:** Önbelleğin içeride nasıl çalıştığını (closure'ın durumu saklaması) görmek için.
- **Test:** `fib(0..24)` sonuçları, önbellek boyutu ve gerçek hesap sayısı (21) `lru_cache` ile aynı.
  Fark: `lru_cache` "en az kullanılanı", `hafiza` "en eski ekleneni" atar.
