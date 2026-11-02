from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/products_db"
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Usuário admin criado automaticamente 
    admin_email: str = "admin@admin.com"
    admin_password: str = "admin123"

    roles_products_read: str = "admin,manager,viewer"
    roles_products_write: str = "admin,manager"
    roles_products_delete: str = "admin"
    roles_users_manage: str = "admin"

    @staticmethod
    def split(value: str) -> list[str]:
        return [r.strip() for r in value.split(",") if r.strip()]


settings = Settings()
