# Sim Hayatı

Bu proje, 1960'ların MS-DOS tarzında bir Sims simülatörüdür. Terminal üzerinde çalışan bu oyunda karakterinizi oluşturup günlük hayatını yönetebilirsiniz.

## Kurulum

Aşağıdaki komutları kullanarak gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

veya doğrudan:

```bash
pip install pyfiglet inquirer rich
```

## Oyunu Başlatma

Oyunu başlatmak için aşağıdaki komutu çalıştırın:

```bash
python main.py
```

## Oyun Özellikleri

- Karakter oluşturma ve özelleştirme
- Temel ihtiyaçları yönetme (yemek, uyku, banyo, sosyalleşme)
- İş ve para yönetimi
- İlişkiler kurma ve geliştirme
- Rastgele olaylar ve durumlar
- Oyun kaydetme ve yükleme

## Kontroller

Oyun tamamen metin tabanlı olup, seçenekler arasında gezinmek için ok tuşlarını ve seçim yapmak için Enter tuşunu kullanabilirsiniz.

## Sınıf Yapısı

- `Sim`: Karakterinizin özelliklerini ve durumunu yöneten sınıf
- `Activity`: Karakterin yapabileceği aktiviteleri tanımlayan sınıf
- `Relationship`: Karakterin diğer karakterlerle ilişkilerini yöneten sınıf
- `Event`: Oyun içinde gerçekleşen rastgele olayları tanımlayan sınıf
- `Game`: Oyun akışını ve kullanıcı arayüzünü yöneten ana sınıf

## İyi Oyunlar! 