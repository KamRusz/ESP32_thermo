from datetime import datetime, timedelta

from app.main import app, db
from app.models import Avg_temphumi, Temphumi
from config import Config

def Average(lst):
    try:
        x = round(sum(lst) / len(lst), 2)
    except ZeroDivisionError:
        return 0
    return x


def timed_job():
    # data = db.session.query(db.func.avg(Temphumi)).filter(Temphumi.day==date.today()).first()
    data = db.session.query(Temphumi).filter(Temphumi.day == datetime.now().strftime("%Y-%m-%d")).all()
    avgt = []
    avgh = []
    for x in data:
        avgt.append(x.temp)
        avgh.append(x.humi)
    u = Avg_temphumi(avg_temp=Average(avgt), avg_humi=Average(avgh))
    if db.session.query(Avg_temphumi).filter(Avg_temphumi.day == datetime.now().strftime("%Y-%m-%d")).all():
        print(datetime.now().strftime("%Y-%m-%d"), "row already exist")
        pass
    else:
        db.session.add(u)
        db.session.commit()
        print(datetime.now().strftime("%Y-%m-%d"), "Avg temperature + humidity row added")
    #deleting old temp data - older then X days
    expendable = datetime.now() - timedelta(days = int(Config.KEEP_LOG_DAYS))
    db.session.query(Temphumi).filter(Temphumi.day < expendable.strftime("%Y-%m-%d")).delete()
    db.session.commit()

if __name__ == "__main__":
    timed_job()

