import os
import requests
import winreg
import vdf
import subprocess
from gdown import download as googledownload
from sys import argv, exit

# Идентификатор игры в Steam
GAME_ID = "1568590"


# Функция для получения пути к установленному Steam из реестра Windows
def get_windows_steam_path() -> str:
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ
    ) as registry_key:
        return (winreg.QueryValueEx(registry_key, "SteamPath"))[0]


# Функция для получения пути к исполняемому файлу Steam из реестра Windows
def get_windows_steam_exe_path() -> str:
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ
    ) as registry_key:
        return (winreg.QueryValueEx(registry_key, "SteamExe"))[0]


# Функция для получения пути к библиотеке Steam, где установлена игра
def get_library_path(steam_path: str, game_id: str) -> str:
    with open(os.path.join(steam_path, r"steamapps\libraryfolders.vdf"), "r") as f:
        data = vdf.load(f)

    library_folders = data.get("libraryfolders", {})

    for library in library_folders.values():
        if ("path" in library) and ("apps" in library) and (game_id in library["apps"]):
            return library["path"]

    raise Exception("Игра не установлена")


# Функция для получения пути к директории игры
def get_game_path(library_path: str) -> str:
    return os.path.join(library_path, r"steamapps\common\Goose Goose Duck")


# Функция для сохранения ответа в .reg файл
def save_response_to_reg_file(reg_path: str, response: requests.Response) -> None:
    with open(reg_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


# Функция для получения ответа от сервера по URL
def get_download_response(url: str) -> requests.Response:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        return r


# Функция для загрузки файла с Google Drive
def download_from_google_drive(url: str, reg_path: str) -> None:
    googledownload(url, reg_path)


# Функция для получения пути к .reg файлу
def get_reg_path(game_path: str) -> str:
    return os.path.join(game_path, r"settings.reg")


# Функция для установки ключей реестра из .reg файла
def set_reg_keys(reg_path: str) -> None:
    try:
        command = ["REG", "IMPORT", reg_path]
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e.stderr}")


# Функция для запуска игры через Steam
def launch_steam_game(steam_exe_path: str, game_id: str) -> None:
    try:
        command = [steam_exe_path, "-applaunch", game_id]
        subprocess.Popen(command)
    except Exception as e:
        print(f"Произошла ошибка {e}")


def main():
    if len(argv) != 2:
        print("Использование: 'python main.py \"downloadlink\"'")
        exit(1)

    if os.name == "nt":
        steam_path = get_windows_steam_path()
        steam_exe_path = get_windows_steam_exe_path()
        library_path = get_library_path(steam_path, GAME_ID)
        game_path = get_game_path(library_path)
        reg_path = get_reg_path(game_path)
        download_from_google_drive(str(argv[1]), reg_path)

        # Следующие две строчки нужны на случай, если пользователь вводит конечную ссылку на скачивание файла
        # response = get_download_response(str(sys.argv[1]))
        # save_response_to_reg_file(reg_path, response)

        set_reg_keys(reg_path)
        launch_steam_game(steam_exe_path, GAME_ID)
    else:
        raise (Exception(f"Операционная система '{os.name}' не поддерживается."))


if __name__ == "__main__":
    main()
