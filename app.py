# -*- coding: utf-8 -*-
"""
Feeder REST Api
"""
import datetime
import json
import os

from bottle import route, run, template, request, static_file

TPL = '''
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>
<b>Last update: {{ts}}</b>

<table>
<tr>
<th>Classe</th>
<th>Ativo</th>
<th>Ult</th>
<th>OCp</th>
<th>OVd</th>
<th>Fech D-0</th>
<th>Fech D-1</th>
<th>Min</th>
<th>Max</th>
<th>Abe</th>
</tr>
%for entry in quotes:
    <tr>
        %for col in entry:
            <td>{{col}}</td>
        %end
    </tr>
%end
</table>
</body>
</html>
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
        # validade json
        if 'timestamp' in request.json.keys():
            _quotes['timestamp'] = excel_dtm_to_str(request.json['timestamp'])
            _quotes['header'] = request.json['header']
            _quotes['data'] = request.json['data']
        print("Update: %s" % _quotes['timestamp'])
    except:
        _quotes['timestamp'] = "bad update"
    return template('<b>Last update: {{ts}}</b>', ts=_quotes['timestamp'])


if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
