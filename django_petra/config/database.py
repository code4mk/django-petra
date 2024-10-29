import os

class DatabaseConfig:
    @classmethod
    def get_database_settings(cls):
        db_engine = os.getenv('DB_CONNECTION', '')
        db_name = os.getenv('DB_DATABASE', '')
        db_user = os.getenv('DB_USERNAME', '')
        db_password = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', '')
        db_port = os.getenv('DB_PORT', '')

        return {
            'ENGINE': cls.get_database_engine(db_engine),
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port,
        }

    @staticmethod
    def get_database_engine(db_engine):
        if db_engine == 'mysql':
            return 'django.db.backends.mysql'
        elif db_engine == 'postgres':
            return 'django.db.backends.postgresql'
        else:
            raise ValueError(f"Unsupported database engine: {db_engine}")

