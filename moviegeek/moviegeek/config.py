import os

from dotenv import load_dotenv

from ep_utils.config_model import ConfigModel

load_dotenv()


class TmdbConfig(ConfigModel):
    api_key: str


TMDB_CONFIG = TmdbConfig()


class MongoConfig(ConfigModel):
    protocol: str = "mongodb"
    user: str
    pwd: str
    host: str
    port: int = 0
    db_name: str
    additional_params: str = ""

    def get_connection_url(self):
        url = f"{self.protocol}://{self.user}:{self.pwd}@{self.host}"
        if self.port:
            url += f":{self.port}"
        url += f"/{self.db_name}"
        if self.additional_params:
            url += self.additional_params
        return url


MONGO_CONFIG = MongoConfig()

if __name__ == "__main__":
    configs = [
        TmdbConfig.get_fields_defaults(),
        MongoConfig.get_fields_defaults(),
    ]

    if os.path.exists("../.env"):
        os.remove("../.env")
    with open("../.env", "w") as file:
        for config in configs:
            file.writelines([f"{k}={v}\n" for k, v in config.items()])
            file.write("\n")
