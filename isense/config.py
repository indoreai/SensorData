import os
import json


class Config:
    USE_SAGEMAKER = os.environ.get('USE_SAGEMAKER', 0)
    print("USE_SAGEMAKER", USE_SAGEMAKER)
    MODE = os.environ.get('MODE')
    if MODE == 'DEVELOPMENT':
        SECRET_KEY = os.environ.get('SECRET_KEY')
        if not SECRET_KEY:
            print("not set environment variable. please set the SECRET KEY environment variable!")
            print("quiting the code")
            exit()
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if not SQLALCHEMY_DATABASE_URI:
            print("not set environment variable. please set the SQLALCHEMY_DATABASE_URI environment variable!")
            print("quiting the code")
            exit()
    else:
       with open('isense/production.json') as f:
            prod_setting = json.load(f)
            SECRET_KEY=prod_setting.get('SECRET_KEY')
            SQLALCHEMY_DATABASE_URI=prod_setting.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.google.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
