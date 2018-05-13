import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuck-you-did-you-guess-for-what'
