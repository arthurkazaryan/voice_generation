# Voice Generation project

## Постановка задачи

Собрать данные, обучить модель синтеза речи на русском языке и разработать веб-сервис и веб-интерфейс для использования модели.
![img.png](misc/img5.png)
## Данные и их сбор

Данные имеют вид пар семплов речи с текстовой транскрибцией.

Сбор производился автоматическими инструментами нарезки по тишине по 5-12 секунд, распознаванием речи, расстановки пунктуации.

## Подготовка окружения
```
git submodule init
git submodule update
docker built -t voice_generation .
docker-compose up

# DJANGO
cd interfaces
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Производительность и необходимое оборудование
Для инференса подойдет CPU. Ryzen 5600h: ~1200 символов в минуту

Для обучения рекомендуется использовать NVIDIA GPU c 16GB VRAM и более. 

Меньше VRAM -> меньше батч сайз -> ниже качество (генерализация) и скорость обучения

## Масштабирование
Решение можно масштабировать: создать оркестр воркеров с помощью, например, kubernetes, и распределенную очередь
## Метрики
Выбраны метрики 

VITS - discriminator loss, generator loss
FastPitch + Univnet - discriminator loss, generator loss, mel loss, vocoder loss
Grad TTS - Prior Loss

## Выбранная модель
По метрикам и аудиовосприятию лучшей моделью избран VITS
## Лог экспериментов

## VITS 
![img_1.png](misc/img_1.png)
## FastPitch + Univnet
![img.png](misc/img.png)
## GradTTS
![img_2.png](misc/img_2.png)