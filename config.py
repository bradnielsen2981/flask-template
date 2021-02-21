class Config:
    DEBUG = True #sets the level of logging to high
    FLASK_ENV = 'development'
    SECRET_KEY = 'my random key can be anything' #required to encrypt Sessions
    JSON = True
    BRICKPI = True
    GROVEPI = True
    EMAIL = False
    CROSSDOMAIN = False
