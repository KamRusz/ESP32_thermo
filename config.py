import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    API_KEY = os.environ.get('API_KEY')
    ADD_USER_KEY = os.environ.get('ADD_USER_KEY')
    TEMP_CHOICES = [
    ('14', 'Min'),
    ('15', '15st'),
    ('16', '16st'),
    ('17', '17st'),
    ('18', '18st'),
    ('19', '19st'),
    ('20', '20st'),
    ('21', '21st'),
    ('22', '22st'),
    ('23', '23st'),
    ('24', '24st'),
    ('25', '25st'),
    ('26', 'Max'),
    ]