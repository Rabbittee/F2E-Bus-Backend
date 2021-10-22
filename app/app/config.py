from pydantic import BaseSettings


class Setting(BaseSettings):
    TDX_HOST: str
    TDX_API_ID: str
    TDX_API_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Setting()
