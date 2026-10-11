# Kapsam (Scope) Örnekleri

> Dersteki 3 örneği kopyala; her biri için önce TAHMİNİNİ yaz, sonra çalıştırıp GERÇEK sonucu yaz.

## Örnek 1
```python
# dersteki kodu buraya yapıştır
```
- **Tahminim:**
- **Gerçek sonuç:**
- **Neden:**

## Örnek 2
(aynı şablon)

## Örnek 3 – UnboundLocalError
```python
sayac = 0
def arttir():
    sayac += 1   # UnboundLocalError
```
- **Tahminim:**
- **Gerçek sonuç:** `UnboundLocalError`
- **Neden:** Fonksiyon içinde `sayac`a atama yapıldığı için Python onu yerel değişken sayar. `+=` önce yerel `sayac`ı okumaya çalışır ama henüz değeri yoktur. Çözüm: `global` değil (bu ödevde yasak), `nonlocal` ile closure kullanmak ya da değeri parametre/dönüş değeriyle taşımak.
