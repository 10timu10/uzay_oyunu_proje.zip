# Dekoratör sırası: `@say` ve `@lru_cache`

Özyinelemeli Fibonacci (`fib(n) = fib(n-1) + fib(n-2)`) için `fib(20)` çağrı sayıları
(kod: `uzay_oyunu/fib_sirasi.py`, çalıştırma: `uv run python -m uzay_oyunu.fib_sirasi`):

| Biçim | Çağrı sayısı |
|---|---|
| Yalnızca `@say` | **21891** |
| `@say` üstte, `@lru_cache` altta | **39** |
| `@lru_cache` üstte, `@say` altta | **21** |

## Önce kural: dekoratörler alttan yukarı uygulanır

```python
@A
@B
def f(): ...      # f = A(B(f))
```

En alttaki `B` fonksiyona en yakın olandır, en üstteki `A` ise **dışarıdan** görünen
nesnedir. Özyineleme `fib(n-1)` yazarken `fib` adını çağrı anında arar ve bu ad
**en üstteki** dekoratörün döndürdüğü nesneye bağlıdır. Yani iç çağrılar da önce
en üstteki katmandan geçer. Sonucu belirleyen budur.

## 1) Yalnızca `@say` → 21891

Önbellek yok, her çağrı gerçekten çalışır. Çağrı sayısı `c(n) = 1 + c(n-1) + c(n-2)`
(`c(0)=c(1)=1`) olur ve bu `2·F(n+1) − 1` değerine eşittir. `n = 20` için
`2·10946 − 1 = 21891`. Aynı alt problemler (örneğin `fib(10)`) defalarca baştan hesaplanır;
bu yüzden çağrı sayısı `n` ile üstel büyür.

## 2) `@say` üstte, `@lru_cache` altta → 39

`fib` adı `say` sarmalayıcısıdır; her `fib(...)` çağrısı, önbellekte olsa bile önce
`say`'dan geçer ve **sayılır**. Önbellek yalnızca altta, gerçek hesabı atlatır:

- `fib(20)` dışarıdan 1 kez çağrılır.
- `n = 20, 19, …, 2` için (19 değer) gövde ilk kez çalışır ve her biri `fib(n-1)` ile
  `fib(n-2)` olmak üzere 2 iç çağrı yapar (bunların çoğu önbellek isabetidir ama yine de sayılır).

Toplam: `1 + 2·19 = 39`. Çağrı sayısı üstelden doğrusala indi, ama `say` isabetleri de gördüğü için
21'e inmedi.

## 3) `@lru_cache` üstte, `@say` altta → 21

`fib` adı artık `lru_cache` nesnesidir. Bir değer önbellekte varsa istek **orada biter**,
altındaki `say`'a hiç ulaşmaz. `say` yalnızca önbellekte olmayan (miss) çağrıları görür:
`n = 0, 1, …, 20` için her biri bir kez, yani **21** (`cache_info().misses` ile aynı sayı).

### Sayaca erişim: `fib.__wrapped__.cagri`

`lru_cache` sarmalayıcısı `functools.wraps` benzeri bir mekanizmayla kurulduğu için
içteki fonksiyonu `__wrapped__` ile gösterir. Gerçek sayaç içteki `say` sarmalayıcısındadır,
bu yüzden `fib.__wrapped__.cagri` kullanılır. `fib.cagri` yazılırsa dekorasyon anında
kopyalanmış eski değer (**0**) okunur; çağrılar arttıkça güncellenmez. Bu yüzden 3. durumda
doğru değer yalnızca `__wrapped__` üzerinden okunur.

## Sonuç

Dekoratör sırası "ne ölçüldüğünü" değiştirir:

- **Önbellek üstteyse** sayaç gerçekten yapılan işi ölçer (21).
- **Sayaç üstteyse** sayaç kullanıcının/özyinelemenin yaptığı tüm istekleri ölçer (39).

Doğru sıra, neyi ölçmek istediğine bağlıdır: hesap maliyeti için önbellek üstte, çağrı trafiği
için sayaç üstte.
