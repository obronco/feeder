# -*- coding: utf-8 -*-
"""
Feeder REST Api
"""
import datetime
import json
import os

from bottle import route, run, template, request

_hour = "n/a"

def excel_dtm_to_str(xldate):
    try:
        xldate = float(xldate)
        xldays = int(xldate)
        frac = xldate - xldays
        seconds = int(round(frac * 86400.0))
        if seconds == 86400:
            seconds = 0
            xldays += 1
        if xldays == 0:
            # second = seconds % 60; minutes = seconds // 60
            minutes, second = divmod(seconds, 60)
            # minute = minutes % 60; hour    = minutes // 60
            hour, minute = divmod(minutes, 60)
            tm = datetime.time(hour, minute, second)
            return tm.strftime('%H:%M:%S')
        else:
            # Excel leap year bug
            dtm = (datetime.datetime.fromordinal(xldays + 693594) +
                   datetime.timedelta(seconds=seconds))

        return dtm.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "N/A"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/feeder', method='GET')
def feeder():
    return template('<b>Last update: {{dtm}}</b>', dtm=_hour)

def update_quotes(q):
    global _hour
    if type(q) is dict and 'Hora' in q.keys():
        # print(q['Hora'])
        _hour = excel_dtm_to_str(q['Hora'])
    else:
        _hour = "bad update"

@route('/update', method='POST')
def update():
    global _hour
    try:
        # Read
        #print(request.json)
        update_quotes(request.json)
    except:
        _hour = "exception"
    return template('<b>Last update: {{dtm}}</b>', dtm=_hour)


if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
