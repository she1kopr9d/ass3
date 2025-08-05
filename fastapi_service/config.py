import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    BROKER_HOST: str
    BROKER_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    TELEGRAM_TOKEN: str
    IP_ADDRESS: str
    PORT: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str = pydantic.Field(alias="POSTGRES_USER")
    DB_PASS: str = pydantic.Field(alias="POSTGRES_PASSWORD")
    DB_NAME: str = pydantic.Field(alias="POSTGRES_DB")

    @property
    def rabbitmq_url(self):
        return (
            f"amqp://{self.RABBITMQ_DEFAULT_USER}:"
            f"{self.RABBITMQ_DEFAULT_PASS}@"
            f"{self.BROKER_HOST}:{self.BROKER_PORT}"
        )

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_psycopg(self):
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
