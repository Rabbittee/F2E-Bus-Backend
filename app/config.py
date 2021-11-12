from pydantic import BaseSettings, Field


class Setting(BaseSettings):
    TDX_HOST: str
    TDX_API_ID: str
    TDX_API_KEY: str
    REDIS_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Setting()
