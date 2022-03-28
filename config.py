import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    )
    API_KEY = os.environ.get("API_KEY")
    ADD_USER_KEY = os.environ.get("ADD_USER_KEY")
    ADD_USER_ALLOWED = os.environ.get("ADD_USER_ALLOWED")
    TEMP_CHOICES = [
        ("14", "Off"),
        ("15", "15°C"),
        ("16", "16°C"),
        ("17", "17°C"),
        ("18", "18°C"),
        ("19", "19°C"),
        ("20", "20°C"),
        ("21", "21°C"),
        ("22", "22°C"),
        ("23", "23°C"),
        ("24", "24°C"),
        ("25", "25°C"),
        ("26", "Max"),
    ]
    TEMP_TRANS = {
        14: "Off",
        15: "15°C",
        16: "16°C",
        17: "17°C",
        18: "18°C",
        19: "19°C",
        20: "20°C",
        21: "21°C",
        22: "22°C",
        23: "23°C",
        24: "24°C",
        25: "25°C",
        26: "Max",
    }
