#!/usr/bin/env python3

import json
from subprocess import Popen, PIPE
from datetime import datetime

import dateutil.parser
import pytz


def run(*cmd):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    return p.communicate()


stdout, stderr = run("git", "log", "--format=%H %aI", "../../0.json")

data = dict()
children = None
tz = pytz.timezone('Asia/Jakarta')

for line in list(stdout.decode('utf-8').splitlines()):
    commit_id, timestamp = line.strip().split()

    ts = dateutil.parser.parse(timestamp)
    ts7 = ts.astimezone(tz)
    dh7 = ts7.strftime('%Y%m%d%H')

    stdout, stderr = run("git", "show", "{}:0.json".format(commit_id))
    data[dh7] = json.loads(stdout.decode('utf-8'))
    children = data[dh7]['children']

#print(json.dumps(children))

cidnames = [(str(c[0]), c[1]) for c in children]
cids = [c[0] for c in cidnames]
cnames = dict(*[cidnames])

hours = sorted(data.keys(), reverse=True)

table = []
for cid in cids:
    row = []
    table.append(row)

    for hour in hours:
        d = data.get(hour, {}).get('data', {}).get(cid, {}).get('sum')
        if not d:
            row.append((None, None))
            continue

        cakupan = d.get('cakupan')
        pending = d.get('pending')
        row.append((cakupan, pending))

ts = datetime.now().isoformat()
result = dict(ts=ts, hours=hours, ids=cids, names=cnames, table=table)
print(json.dumps(result))
