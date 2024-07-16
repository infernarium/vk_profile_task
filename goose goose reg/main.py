import os, requests, winreg, vdf, subprocess, sys


GAME_ID = "1568590"

def get_windows_steam_path()->str:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ) as registry_key:
        return (winreg.QueryValueEx(registry_key, "SteamPath"))[0]
    
def get_windows_steam_exe_path()->str:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ) as registry_key:
        return (winreg.QueryValueEx(registry_key, "SteamExe"))[0]  
    
def get_library_path(steam_path: str, game_id: str)->str:
    with open(os.path.join(steam_path, r"steamapps\libraryfolders.vdf"), "r") as f:
        data = vdf.load(f)
        
    library_folders = data.get('libraryfolders', {})
    
    for library in library_folders.values():
        if ('path' in library) and ('apps' in library) and (game_id in library['apps']):
            return library['path']
    
    return None # TODO:сделать исключением

def get_game_path(library_path: str)->str:
    return os.path.join(library_path, r"steamapps\common\Goose Goose Duck")
    
def download(reg_path: str, url: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(reg_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)      
                
def get_reg_path(game_path: str)->str:
    return os.path.join(game_path, r"settings.reg")

def set_reg_keys(reg_path: str):
    try:
        command = ['REG', 'IMPORT', reg_path]
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e.stderr}")
           
def launch_steam_game(steam_exe_path: str, game_id: str):
    try:
        command = [steam_exe_path, '-applaunch', game_id]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка {e.stderr}")
        
def main():
    if len(sys.argv) != 2:
        print("Использование: 'python main.py downloadlink'")
        sys.exit(1)
        
    if os.name == "nt":
        steam_path = get_windows_steam_path()
        steam_exe_path = get_windows_steam_exe_path()
        library_path = get_library_path(steam_path, GAME_ID)
        game_path = get_game_path(library_path)
        reg_path = get_reg_path(game_path)
        download(reg_path, str(sys.argv[1]))
        set_reg_keys(reg_path)
        launch_steam_game(steam_exe_path, GAME_ID)
    else:
        raise(Exception(f"Операционная система '{os.name}' не поддерживается."))
    
    
if __name__ == "__main__":
    main()
    