from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Notes'
    app_description: str = 'App_for_Notes'
    database_url: str

    class Config:
        env_file = '.env'

settings = Settings()