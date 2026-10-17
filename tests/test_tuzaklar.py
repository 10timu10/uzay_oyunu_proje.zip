from uzay_oyunu.tuzaklar import yakit_ekle


def test_depo_cagrilar_arasinda_paylasilmaz():
    assert yakit_ekle(5) == [5]
    assert yakit_ekle(7) == [7]  # hatalı sürümde [5, 7] çıkar


def test_verilen_depo_kullanilir():
    depo = [1]
    assert yakit_ekle(2, depo) == [1, 2]
