import configparser


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('serverconfig.ini')

        self.ControlPasswordHash = self.config["PasswordHash"]
        