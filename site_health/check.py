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

import json
import requests
import os
import sqlite3
import hashlib
import string
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

def name_to_key(name):
    punc = unicode(string.punctuation)
    replace_punctuation = string.maketrans(punc, '_'*len(punc))
    return str(name).translate(replace_punctuation)

def record_run(db, run_id):
    csr = db.cursor()
    csr.execute("""
      insert into run 
        (run_id) 
      values
        (?)
    """, (run_id, ))


def record_request(db, name, run_id, status_code, duration, size, hash):
    csr = db.cursor()
    csr.execute("""
      insert into endpoint_test 
        (name, run_id, status_code, duration, size, hash) 
      values
        (?, ?, ?, ?, ?, ?)
    """, (name, run_id, status_code, duration, size, hash))


def test_request(db, run_id, endpoint):
    key = name_to_key(endpoint["name"])
    req = endpoint["request"]
    url = None
    if "url" in req:
        url = req["url"]["raw"]
    elif "raw" in req:
        url = req["raw"]
    else:
        raise Exception("no url found in " + key)

    out_file = "{}/{}.txt".format(run_id, key)
    method = req["method"]
    resp = None
    t0 = datetime.now()
    headers = {}
    auth=None
    if "auth" in req:
        username = None
        password = None
        for auth_item in req["auth"]["basic"]:
            if auth_item["key"] == "username":
                username = auth_item["value"]
            if auth_item["key"] == "password":
                password = auth_item["value"]
        auth=HTTPBasicAuth(username, password)

    if "header" in req:
        for header_item in req["header"]:
            headers[header_item["key"]] = header_item["value"]

    data = None                
    if method == "POST":
        data = req["body"]["raw"]
    resp = requests.request(method, url, data=data, auth=auth, headers=headers)
    
    duration = ((datetime.now() - t0).microseconds)/1000
    print("{} {}".format(key, resp.status_code))
    resp_content = None
    if resp.status_code == 200:
        parsed = json.loads(resp.text)
        resp_content = json.dumps(parsed, indent=4)
    else:
        resp_content = resp.text
    size = len(resp.content)
    hash = hashlib.sha1(resp.content).hexdigest()
    with open(out_file, 'w') as out:
        out.write(resp_content)
    record_request(db, key, run_id, resp.status_code, duration, size, hash)


if __name__ == '__main__':
    db = sqlite3.connect('results.db')
    api_endpoints_file = open('yangcatalog.postman_collection.json')
    api_endpoints = json.load(api_endpoints_file)
    now = datetime.now()
    run_id = now.strftime("%Y%m%d-%H%M%S")
    os.mkdir(run_id)
    record_run(db, run_id)
    for item in api_endpoints["item"]:
        test_request(db, run_id, item)
    db.commit()
