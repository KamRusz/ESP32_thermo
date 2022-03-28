from datetime import datetime, date
from apscheduler.schedulers.blocking import BlockingScheduler
from app.main import app, db
from app.models import Temphumi, Avg_temphumi

sched = BlockingScheduler()

def Average(lst):
    try: 
        x = round(sum(lst) / len(lst),2)
    except ZeroDivisionError:
        return 0
    return x

x=str(datetime.now())
        

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print("datetime.now()[:10]", x[:10])
    print("date.today()",date.today())
    print('datetime.today().strftime("%Y-%m-%d")',datetime.today().strftime("%Y-%m-%d"))

'''
@sched.scheduled_job('cron', hour=23)
def timed_job():
    data = db.session.query(Temphumi).filter(Temphumi.day==datetime.today().strftime("%Y-%m-%d")).#grupowanie średnia all()
    avgt=[]
    avgh=[]
    for x in data:
        avgt.append(x.temp)
        avgh.append(x.humi)
    u = Avg_temphumi(avg_temp = Average(avgt), avg_humi=Average(avgh))
    if db.session.query(Avg_temphumi).filter(Avg_temphumi.day==datetime.today().strftime("%Y-%m-%d")).all():
        pass
    else:
        db.session.add(u)
        db.session.commit()
'''


sched.start()