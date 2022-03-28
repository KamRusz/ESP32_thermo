from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from app.main import app, db
from app.models import Avg_temphumi, Temphumi

sched = BlockingScheduler()


def Average(lst):
    try:
        x = round(sum(lst) / len(lst), 2)
    except ZeroDivisionError:
        return 0
    return x


@sched.scheduled_job("cron", hour=23)
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
        pass
    else:
        db.session.add(u)
        db.session.commit()
    #deleting old temp data - 2 days before today
    expendable = datetime.now() - timedelta(days = 2)
    db.session.query(Temphumi).filter(Temphumi.day == expendable.strftime("%Y-%m-%d")).delete()
    db.session.commit()

sched.start()
