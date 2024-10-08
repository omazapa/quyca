import os
from functools import lru_cache
from typing import Optional
from dotenv import dotenv_values
from typing_extensions import Self
from pydantic import model_validator, MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: dict = {}
    if os.getenv("ENVIRONMENT") == "dev":
        env = dotenv_values(".env.dev")
    elif os.getenv("ENVIRONMENT") == "prod":
        env = dotenv_values(".env.prod")

    APP_NAME: str = env["APP_NAME"]
    APP_VERSION: str = env["APP_VERSION"]
    APP_DEBUG: bool = env["APP_DEBUG"]
    APP_PORT: str | int = env["APP_PORT"]
    APP_DOMAIN: str = env["APP_DOMAIN"]
    APP_ENVIRONMENT: str = env["APP_ENVIRONMENT"]

    APP_V1_STR: str = env["APP_V1_STR"]
    APP_V2_STR: str = env["APP_V2_STR"]
    API_V1_STR: str = env["API_V1_STR"]
    API_V2_STR: str = env["API_V2_STR"]

    MONGO_SERVER: str = env["MONGO_SERVER"]
    MONGO_INITDB_ROOT_USERNAME: str = env["MONGO_INITDB_ROOT_USERNAME"]
    MONGO_INITDB_ROOT_PASSWORD: str = env["MONGO_INITDB_ROOT_PASSWORD"]
    MONGO_INITDB_DATABASE: str = env["MONGO_INITDB_DATABASE"]
    MONGO_INITDB_PORT: int = env["MONGO_INITDB_PORT"]
    MONGO_IMPACTU_DB: str = env["MONGO_IMPACTU_DB"]

    MONGO_URI: Optional[MongoDsn] = None

    @model_validator(mode="after")
    def validate_mongo_uri(self) -> Self:
        self.MONGO_URI = MongoDsn.build(
            scheme="mongodb",
            host=self.MONGO_SERVER,
            username=self.MONGO_INITDB_ROOT_USERNAME,
            password=self.MONGO_INITDB_ROOT_PASSWORD,
            port=self.MONGO_INITDB_PORT
        )
        return self

    EXTERNAL_IDS_MAP: dict[str, str] = {
        "scholar": "https://scholar.google.com/scholar?hl="
        "en&as_sdt=0%2C5&q=info%3A{id}%3Ascholar.google.com",
        "doi": "https://doi.org/{id}",
        "lens": "https://www.lens.org/lens/scholar/article/{id}",
        "minciencias": "",
        "scienti": "",
    }

    TYPES: dict[str, str] = {
        "peer-review": "Revisión por partes",
        "techreport": "Informe técnico",
        "masterthesis": "Tesis de maestría",
        "dataset": "Conjunto de datos",
        "editorial": "Editorial",
        "Publicado en revista especializada": "Publicado en revista especializada",
        "report": "Informe",
        "Artículos": "Artículos",
        "letter": "Carta",
        "Corto (resumen)": "Resumen",
        "reference-entry": "Entrada de referencia",
        "dissertation": "Disertación",
        "standard": "Estándar",
        "Artículos de investigación": "Artículos de investigación",
        "Artículo": "Artículo",
        "incollection": "En colección",
        "book": "Libro",
        "article": "Artículo",
        "Caso clínico": "Caso clínico",
        "paratext": "Paratexto",
        "misc": "Misceláneo",
        "erratum": "Errata",
        "Revisión (Survey)": "Revisión",
        "inproceedings": "En actas",
    }

    institutions: list[str] = [
        "Archive",
        "Company",
        "Education",
        "Facility",
        "Government",
        "Healthcare",
        "Nonprofit",
        "Other",
        "archive",
        "company",
        "education",
        "facility",
        "government",
        "healthcare",
        "nonprofit",
        "other",
        "institution"
    ]


@lru_cache()
def get_settings() -> BaseSettings:
    """Get the settings for the application."""
    return Settings()


settings: Settings = Settings()
