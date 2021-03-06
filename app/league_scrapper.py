import json
import os
import shutil

import aiohttp
import requests
import urllib3

from app.exceptions import ClientDisconnectedError, LeagueClientClosedError

if os.name == "nt":
    import wmi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LeagueToolBelt:
    def __init__(self):
        self.base_url = "https://127.0.0.1"
        self.lockfile_name = "lockfile"
        self.install_dir = None
        self.port = None
        self.auth = None
        self.version = None
        self.cache_dir = "./app/resources/cache"

        self.__set_initial_data()
        self.version_check()

    @staticmethod
    def __get_client_process_info():
        c = wmi.WMI()
        install_dir, port = None, None
        for process in c.Win32_Process():
            if process.name == "LeagueClientUx.exe":
                cmd = process.CommandLine
                for segment in cmd.split('" "'):
                    if "--app-port" in segment:
                        port = segment.split("=")[1]
                    if "--install-directory" in segment:
                        install_dir = segment.split("=")[1]
                break
        else:
            raise LeagueClientClosedError(
                "The League of Legends Client is not running!"
            )
        return install_dir, port

    def __get_lockfile_data(self):
        path = os.path.join(self.install_dir, self.lockfile_name)
        try:
            with open(path) as f:
                lockfile = f.read()
            lockfile = lockfile.split(":")
            process_name, process_ID, _port, password, protocol = lockfile
        except FileNotFoundError:
            raise LeagueClientClosedError(
                "The League of Legends Client is not running!"
            )

        _auth = aiohttp.BasicAuth("riot", password).encode()
        return _port, _auth

    def __set_initial_data(self):
        if not os.path.exists(f"{self.cache_dir}/install_dir.txt"):
            self.install_dir, self.port = self.__get_client_process_info()
            with open(f"{self.cache_dir}/install_dir.txt", "w") as f:
                f.write(self.install_dir)
        else:
            with open(f"{self.cache_dir}/install_dir.txt", "r") as f:
                _install_dir = f.read()
            if len(_install_dir) != 0:
                self.install_dir = _install_dir
            else:
                os.remove(f"{self.cache_dir}/install_dir.txt")
                self.__set_initial_data()

        self.port, self.auth = self.__get_lockfile_data()

    def get(self, endpoint: str):
        _port, _auth = self.__get_lockfile_data()
        r = requests.get(
            f"{self.base_url}:{_port}{endpoint}",
            headers={"Accept": "application/json", "Authorization": _auth},
            verify=False,
        )
        return r, r.json()

    def post(self, endpoint: str, data: dict = None):
        _port, _auth = self.__get_lockfile_data()
        r = requests.post(
            f"{self.base_url}:{_port}{endpoint}",
            headers={"Accept": "application/json", "Authorization": _auth},
            data=data,
            verify=False,
        )
        return r

    def connection_check(self):
        _port, _auth = self.__get_lockfile_data()
        is_connected = requests.get(
            f"{self.base_url}:{_port}/lol-platform-config/v1/initial-configuration-complete",
            headers={"Accept": "application/json", "Authorization": _auth},
            verify=False,
        )
        return is_connected.json()

    def version_check(self):
        with open(f"{self.cache_dir}/champ_info.json", encoding="utf8") as f:
            current_cached_json = json.load(f)
            current_cached_game_version = current_cached_json["version"]

        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        current_json = json.loads(response.text)
        current_game_version = current_json[0]
        self.version = current_game_version

        if current_cached_game_version != current_game_version:
            response = requests.get(
                f"http://ddragon.leagueoflegends.com/cdn/{self.version}"
                f"/data/en_US/champion.json"
            )
            new_json = json.loads(response.text)
            self.__champion_check(current_cached_json, new_json)
            with open(f"{self.cache_dir}/champ_info.json", "w") as f:
                json.dump(new_json, f)

    def __champion_check(self, current_cached_json, current_json):
        cached_champ_list = current_cached_json["data"].keys()
        current_champ_list = current_json["data"].keys()

        if cached_champ_list != current_champ_list:
            for champ in current_champ_list:
                response = requests.get(
                    f"http://ddragon.leagueoflegends.com/cdn/{self.version}"
                    f"/img/champion/{champ}.png",
                    stream=True,
                )
                with open(f"{self.cache_dir}/champ_img/{champ}.png", "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
