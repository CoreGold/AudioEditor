# Редактор аудио
Программа предназначена для базового редактирования аудиофайлов, включая обрезку, изменение скорости воспроизведения и громкости.

## Функции
- Импорт аудио: загрузка файла для редактирования.
- Обрезка: выбор начала и конца фрагмента для сохранения.
- Изменение скорости воспроизведения: регулировка скорости воспроизведения аудио.
- Изменение громкости: увеличение или уменьшение громкости.
- Экспорт аудио: сохранение отредактированного файла.
- Отмена изменений: возможность откатить последнее действие.

## Использование FFmpeg
Для обработки аудиофайлов программа использует библиотеку FFmpeg. FFmpeg является мощным инструментом с открытым исходным кодом для обработки аудио и видео.

### Зачем используется FFmpeg?
Для обеспечения высокопроизводительных операций с аудио, таких как обрезка, изменение скорости и громкости.

### Указание лицензии FFmpeg
FFmpeg распространяется под лицензией LGPL или GPL (в зависимости от сборки). Для получения информации о лицензии вы можете ознакомиться с официальным сайтом FFmpeg.

## Установка
### Требования
- Операционная система: Windows
- FFmpeg. Вы можете скачать ее с официального сайта FFmpeg.
- Форматы аудио: MP3, WAV

### 1. Использование собранного приложения
1.1 Скачайте архив с приложением по следующей [ссылке](https://drive.google.com/file/d/1BzCB5yTdNaRBimUruHWT6554h1y3g5lY/view?usp=sharing)

1.2 Разархивируйте приложение в удобное место

1.3 Запускайте программу через main.exe

1.4 Можно приступать к работе

### 2. Самостоятельная сборка проекта
2.1 Скачайте ветку "release"

2.2 Скачайте FFmpeg с официального сайта

2.3 Поместите папку "bin", содержащую файлы ffmpeg.exe и ffprobe.exe, в директорию проекта

2.4 Создайте папку "Temp" в директории проекта

2.5 Используйте желаемый инструмент сборки python файла, например pyinstaller

## Инструкция по использованию
### 1. Импорт аудио
Нажмите кнопку Импорт.
Выберите аудиофайл из вашего компьютера.
### 2. Воспроизведение
Нажмите кнопку ▶ для воспроизведения.
Используйте кнопки ⏸ для паузы и ⏹ для остановки.
### 3. Обрезка аудио
В блоке Обрезать задайте начальное и конечное время (в формате мм:сс).
Нажмите кнопку Применить, чтобы сохранить изменения.
### 4. Изменение скорости воспроизведения
В блоке Изменить скорость воспроизведения переместите ползунок, чтобы задать желаемую скорость (например, 100 = нормальная скорость).
Нажмите Применить.
### 5. Изменение громкости
В блоке Изменить громкость укажите желаемое значение в децибелах (дБ).
Нажмите Применить.
### 6. Экспорт аудио
Нажмите кнопку Экспорт, чтобы сохранить редактированный файл.
### 7. Отмена изменений
Если вы хотите отменить последнее действие, нажмите кнопку Шаг назад.

## Лицензия
Программа распространяется бесплатно и предназначена для личного использования. Подробнее в LICENSE.md.

### Благодарности
Благодарность команде разработчиков FFmpeg за предоставление мощного и универсального инструмента для работы с мультимедиа.
