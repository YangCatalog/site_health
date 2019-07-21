#!/usr/bin/env python
# Copyright The IETF Trust 2019, All Rights Reserved
# Copyright 2019 Douglas Hubler
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Douglas Hubler"
__copyright__ = "Copyright 2019 Douglas Hubler, Copyright The IETF Trust 2019, All Rights Reserved"
__license__ = "Apache License, Version 2.0"
__email__ = "douglas@hubler.us"

import os
import sqlite3
import json
from flask import Flask

app = Flask(__name__)
db = sqlite3.connect('results.db')

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/run')
def runs():
    csr = db.cursor()
    q = "select run_id, timestamp from run order by run_id desc limit 20"
    runs = []
    for row in csr.execute(q):
        run_id, timestamp = row
        runs.append({
            "run_id" : run_id,
            "timestamp" : timestamp,
        })
    return json.dumps({"runs" : runs})

@app.route('/endpoint')
def endpoints():
    csr = db.cursor()
    q = "select distinct name from endpoint_test order by name"
    endpoints = []
    for row in csr.execute(q):
        endpoints.append(row)
    return json.dumps({"endpoints" : endpoints})


@app.route('/endpoint/<name>')
def endpoint(name):
    csr = db.cursor()
    q = """
      select
        endpoint_test.run_id,
        run.timestamp,
        endpoint_test.name,
        endpoint_test.status_code,
        endpoint_test.duration,
        endpoint_test.size,
        endpoint_test.hash
      from 
        run, endpoint_test
      where 
        run.run_id = endpoint_test.run_id 
        and endpoint_test.name = ?
    """
    runs = []
    endpoint = {
        "runs" : runs
    }
    for row in csr.execute(q, (name, )):
        run_id, timestamp, name, status_code, duration, size, hash = row
        endpoint["name"] = name
        runs.append({
            "run_id" : run_id,
            "timestamp" : timestamp,
            "status_code" : status_code,
            "duration" : duration,
            "size" : size,
            "hash" : hash,
        })
    return json.dumps(run)

@app.route('/run/<run_id>')
def run(run_id):
    csr = db.cursor()
    q = """
      select
        run.run_id,
        run.timestamp,
        endpoint_test.name,
        endpoint_test.status_code,
        endpoint_test.duration,
        endpoint_test.size
      from 
        run, endpoint_test
      where 
        run.run_id = endpoint_test.run_id
    """
    endpoint_test = []
    run = {
        "endpoint_tests" : endpoint_test
    }
    for row in csr.execute(q):
        run_id, timestamp, name, status_code, duration, size = row
        run["run_id"] = run_id
        run["timestamp"] = timestamp
        endpoint_test.append({
            "name" : name,
            "status_code" : status_code,
            "duration" : duration,
            "size" : size,
        })
    return json.dumps(run)
