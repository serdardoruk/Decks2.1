from base64 import b64encode

# this was generated with os.urandom(24) but we can change this occasionally for more security
secret_key = b64encode(b'\xfcu\xa4\xfa9\xdd\x83!b\x9d\x84\x89-\xc1\x01v\x95\xdeL4\xfa\xba\xc4\x07')
secret_key = secret_key.decode('utf-8')


class BaseConfig(object):
    DEBUG = True
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "postgres://tdmlcuezwsdofb:9ff3b9b3c4dce3aa38e54773fe2231149286280f509fb6058a1e2216cb0b6bab@ec2-50-17-250-38.compute-1.amazonaws.com:5432/d8c0s19dqcv18k"
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)"
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///py/data/database/test_database.db"
    SECRET_KEY = secret_key

class DevelopmentConfig(BaseConfig):
    SECRET_KEY = secret_key
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "postgres://tdmlcuezwsdofb:9ff3b9b3c4dce3aa38e54773fe2231149286280f509fb6058a1e2216cb0b6bab@ec2-50-17-250-38.compute-1.amazonaws.com:5432/d8c0s19dqcv18k"
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)"
    SQLALCHEMY_DATABASE_URI = "sqlite:///py/data/database/test_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(BaseConfig):
    
    SECRET_KEY = secret_key
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "postgres://tdmlcuezwsdofb:9ff3b9b3c4dce3aa38e54773fe2231149286280f509fb6058a1e2216cb0b6bab@ec2-50-17-250-38.compute-1.amazonaws.com:5432/d8c0s19dqcv18k"
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)"
    SQLALCHEMY_DATABASE_URI = "sqlite:///py/data/database/test_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False