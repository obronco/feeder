# -*- coding: utf-8 -*-
"""
Feeder REST Api
"""
import datetime
import json
import os

from bottle import route, run, template, request, static_file  #, hook, response

_quotes = {'timestamp': 'n/a', 'data': []}

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
        return "n/a"

# @hook('after_request')
# def enable_cors():
#     """
#     You need to add some headers to each request.
#     Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
#     """
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST'
#     response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

# @route('/feeder', method='GET')
# def feeder():
#     return template(TPL, ts=_quotes['timestamp'], quotes=_quotes['data'])
@route('/feeder')
def feeder():
    return static_file('feeder.html', root='.')

@route('/getquotes')
def get_quotes():
    return _quotes

@route('/update', method='POST')
def update():
    global _quotes
    try:
        _aux = {}
        # check for keys
        if ('data' in request.json.keys() and
            'header' in request.json.keys() and
            'timestamp' in request.json.keys()):
            _aux['timestamp'] = excel_dtm_to_str(request.json['timestamp'])
            _aux['header'] = request.json['header']
            _aux['data'] = request.json['data']
        # validade json
        print(_aux['data'][0])
        if (len(_aux['header']) > 0 and
            (len(_aux['header']) == len(_aux['data'][0])) and
            _aux['timestamp'] != 'n/a'):
            # success
            _quotes = _aux
            print("Update: %s" % _quotes['timestamp'])
        else:
            print("invalid data")
    except:
        print("update failed")

    return template('<b>Last update: {{ts}}</b>', ts=_quotes['timestamp'])


if __name__ == '__main__':
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=5000, debug=True)
    # run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
