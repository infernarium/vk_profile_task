### README

## Формулировка задачи

Необходимо написать скрипт, который:

- По приложенной ссылке скачивает файл
- Вносит значения из файла в реестр Windows
- Запускает Steam или игру

Дополнительно: Скрипт должен работать на машине проверяющего, вне зависимости от расположения дистрибутива игры.

## Требования

- Windows OS
- Python 3.6+
- Установленные модули Python:
  - `requests`
  - `vdf`
  - `gdown`

## Установка

1. **Клонируйте репозиторий или скачайте архив с проектом:**

   ```bash
   git clone https://github.com/infernarium/vk_profile_task
   cd vk_profile_task/goose goose reg/
   ```

2. **Установите необходимые зависимости:**

   ```bash
   pip install requirements.txt
   ```

## Использование

1. **Запустите скрипт с указанием ссылки на Google Drive:**

   ```bash
   python main.py "https://drive.google.com/uc?export=download&id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH"
   ```

   **Примечание:** Убедитесь, что ссылка правильная и указывает на существующий и общедоступный файл из Google Drive.

## Обзор кода

### Импортируемые модули

- `os`: Для работы с файловой системой.
- `requests`: Для выполнения HTTP-запросов.
- `winreg`: Для работы с реестром Windows.
- `vdf`: Для чтения файлов VDF (Valve Data Format).
- `subprocess`: Для выполнения системных команд.
- `sys`: Для работы с аргументами командной строки.
- `gdown`: Для загрузки файлов с Google Drive.

### Константы

- `GAME_ID`: Идентификатор игры в Steam.

### Функции

- `get_windows_steam_path()`: Получает путь к установленному Steam из реестра Windows.
- `get_windows_steam_exe_path()`: Получает путь к исполняемому файлу Steam из реестра Windows.
- `get_library_path(steam_path, game_id)`: Получает путь к библиотеке Steam, где установлена игра.
- `get_game_path(library_path)`: Получает путь к директории игры.
- `save_response_to_reg_file(reg_path, response)`: Сохраняет ответ HTTP-запроса в файл .reg.
- `get_download_response(url)`: Выполняет HTTP-запрос и возвращает его ответ.
- `download_from_google_drive(url, reg_path)`: Загружает файл с Google Drive.
- `get_reg_path(game_path)`: Получает путь к .reg файлу.
- `set_reg_keys(reg_path)`: Импортирует ключи реестра из файла .reg.
- `launch_steam_game(steam_exe_path, game_id)`: Запускает игру через Steam.

### Основная функция `main()`

1. Проверяет аргументы командной строки.
2. Получает пути к Steam и игре.
3. Загружает файл настроек с Google Drive.
4. Импортирует ключи реестра из файла настроек.
5. Запускает игру через Steam.

## Примечания

- Скрипт поддерживает только операционную систему Windows.
- На текущий момент загрузка происходит только из Google Drive.
- Важно чтобы у пользователя был установлен стим и игра.
- функция `download_from_google_drive` на текуший момент работает через функцию библиотеки `gdown`
