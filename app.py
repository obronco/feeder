# -*- coding: utf-8 -*-
"""
Feeder REST Api
"""
import datetime
import json
import os

from bottle import route, run, template, request

TPL = '''
<b>Last update: {{ts}}</b>

<table border="1">
<tr>
<td><b>Classe</b></td>
<td><b>Ativo</b></td>
<td><b>Ult</b></td>
<td><b>OCp</b></td>
<td><b>OVd</b></td>
<td><b>Fech D-0</b></td>
<td><b>Fech D-1</b></td>
<td><b>Min</b></td>
<td><b>Max</b></td>
<td><b>Abe</b></td>
</tr>
%for entry in quotes:
    <tr>
        %for col in entry:
            <td>{{col}}</td>
        %end
    </tr>
%end
</table>
'''

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
        return "invalid timestamp"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/feeder', method='GET')
def feeder():
    return template(TPL, ts=_quotes['timestamp'], quotes=_quotes['data'])

@route('/update', method='POST')
def update():
    global _quotes
    try:
        print(request.json['timestamp'])
        # validade json
        if 'timestamp' in request.json.keys():
            _quotes['timestamp'] = excel_dtm_to_str(request.json['timestamp'])
            _quotes['data'] = request.json['data']
    except:
        _quotes['timestamp'] = "bad update"
    return template('<b>Last update: {{ts}}</b>', ts=_quotes['timestamp'])


if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
