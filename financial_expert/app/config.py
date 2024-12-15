import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-testing'
    WTF_CSRF_ENABLED = True