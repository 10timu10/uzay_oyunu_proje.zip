# Kapsam (Scope) Örnekleri
Python bir isim ararken sırayla şu kapsamlara bakar (LEGB kuralı):
**L**ocal (yerel) → **E**nclosing (çevreleyen fonksiyon) → **G**lobal (modül) → **B**uilt-in (yerleşik).

## Örnek 1 – Yerel değişken globali gölgeler
```python
x = "global"

def goster():
    x = "yerel"
    print(x)

goster()
print(x)
```
- **Tahminim:** Önce `yerel`, sonra `global` yazdırır. Fonksiyon içindeki `x` ayrı bir değişken olduğu için dıştaki `x`i değiştirmez.
- **Gerçek sonuç:**
  ```
  yerel
  global
  ```
- **Neden:** Fonksiyon içinde `x = "yerel"` ataması yapıldığı için Python yeni bir **yerel** `x` oluşturur. Bu yerel `x`, aynı adlı globali yalnızca fonksiyon boyunca gölgeler; globaldeki `x` hiç değişmez. Fonksiyon bitince yerel `x` yok olur ve `print(x)` globali yazar.

## Örnek 2 – Closure ve `nonlocal` (projedeki `hamle_sayaci`)
```python
def sayac_olustur():
    sayi = 0

    def arttir():
        nonlocal sayi
        sayi += 1
        return sayi

    return arttir

s = sayac_olustur()
print(s(), s(), s())
```
- **Tahminim:** `1 2 3`. `sayac_olustur` bittikten sonra bile iç fonksiyon `sayi` değerini hatırlar ve her çağrıda bir artırır.
- **Gerçek sonuç:** `1 2 3`
- **Neden:** `arttir`, çevreleyen fonksiyondaki `sayi` değişkenini **closure** ile yakalar. `sayac_olustur` döndükten sonra bile `sayi` bellekte kalır, çünkü `arttir` ona hâlâ başvurur. `nonlocal sayi` olmasaydı `sayi += 1` yerel bir değişken yaratmaya çalışır ve hata verirdi (Örnek 3). `nonlocal`, atamanın çevreleyen kapsamdaki `sayi`ya yapılmasını sağlar. Aynı yapı projedeki `hamle_sayaci()` fonksiyonunda kullanılıyor ve `global` kullanmaya gerek bırakmıyor.

## Örnek 3 – UnboundLocalError
```python
sayac = 0
def arttir():
    sayac += 1   # UnboundLocalError
```
- **Tahminim:** Global `sayac` zaten var, bu yüzden `sayac += 1` onu bir artırır ve hata vermez.
- **Gerçek sonuç:** `UnboundLocalError` (`cannot access local variable 'sayac' where it is not associated with a value`)
- **Neden:** Fonksiyon içinde `sayac`a atama yapıldığı için Python onu yerel değişken sayar. `+=` önce yerel `sayac`ı okumaya çalışır ama henüz değeri yoktur. Çözüm: `global` değil (bu ödevde yasak), `nonlocal` ile closure kullanmak ya da değeri parametre/dönüş değeriyle taşımak.

