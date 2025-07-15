class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = True

class LocalDevelopmentConfig(Config):
    #configration for db
    SQLALCHEMY_DATABASE_URI = "sqlite:///securedb.sqlite3"
    DEBUG = True

    #configration for Security
    SECRET_KEY  = "this-is-a-secret-key"#hash use credemtials and store ijn seesion
    SECURITY_PASSWORD_HASH = "bcrypt"#mechenism to hash credentials and store in database
    SECURITY_PASSWORD_SALT = "this-is-a-salt-key"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
 