from ep_utils.config_model import ConfigModel


class PostgresConfig(ConfigModel):
    user: str
    pwd: str
    host: str
    port: int = 5432
    db_name: str = ""
    ssl: bool = False

    def get_connection_url(self):
        string = f"postgres://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db_name}"
        if self.ssl:
            string += "?sslmode=require"
        return string


