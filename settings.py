import ftplib

server_url = "https://gabrielwawerski.github.io/FinanceMate/"
data_dir = "data/"
full_data_url = server_url + data_dir
default_settings = "settings_default.json"


ftp_username = "epiz_27836100"
ftp_password = "agipcompany"
ftp_host = "ftp.epizy.com"

ftp = ftplib.FTP(ftp_host, ftp_username, ftp_password)


class Settings:
    def __init__(self):
        self.settings = {}

    def get_setting(self, name):
        print(f"getting {name}")
        return self.settings[name]

    def set_setting(self, setting, value):
        print(f"[Settings Change] {setting}: {self.get_setting(setting)} -> {value}")
        if setting in self.settings:
            self.settings[setting] = value
        else:
            print(f"No such setting: {setting}")

    def add_setting(self, setting, value):
        self.settings[setting] = value

    def _add_settings(self, **args):
        for k, v in args.items():
            self.settings[k] = v

    def __call__(self, *args, **kwargs):
        return self.settings

    def load(self, settings):
        self.settings = settings


app_settings = Settings()



