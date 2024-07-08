import os

class config:
    mongo_db_url = "mongodb://{}:{}@{}:{}/{}?authSource=admin&retryWrites=true&w=majority".format(
                                                    os.getenv('MONGO_USERNAME', "admin"),
                                                    os.getenv('MONGO_PASSWORD', "admin"),
                                                    os.getenv('MONGO_HOST', "localhost"),
                                                    os.getenv('MONGO_PORT', 27017),
                                                    os.getenv('MONGO_DBNAME_ALIAS', "tal2k"))


    database_name = os.getenv('MONGO_DBNAME_ALIAS')

    secret_key = os.getenv('SECRET_KEY')

    sqlalchemy_database_uri = "postgresql://{}:{}@{}:{}/{}".format(os.getenv('POSTGRES_USERNAME', "admin"),
                                                                os.getenv('POSTGRES_PASSWORD', "admin"),
                                                                os.getenv('POSTGRES_HOST', "localhost"),
                                                                os.getenv('POSTGRES_PORT', 5432),
                                                                os.getenv('POSTGRES_DBNAME_ALIAS', "tal2k"))
    
    celery_broker_url = os.getenv('CELERY_BROKER_URL', "redis://localhost:6379")
    celery_result_backend = os.getenv('CELERY_RESULT_BACKEND', "redis://localhost:6379")