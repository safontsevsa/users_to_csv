# Yandex 360 User Export

Экспорт пользователей из организации Яндекс 360 в CSV для последующей миграции в другую организацию.

## Возможности

- Выгружает всех сотрудников вашей организации в CSV-файл по заданному формату.
- Формирует столбцы:
  - login
  - password (генерируется временный случайный)
  - password_change_required
  - first_name
  - last_name
  - middle_name
  - position
  - gender
  - birthday
  - language
  - phone
- Безопасно работает с токеном через файл `.env`.

## Быстрый старт

### 1. Клонируйте репозиторий и установите зависимости

```bash
git clone https://github.com/yourname/yandex-360-export.git
cd yandex-360-export
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
