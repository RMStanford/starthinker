###########################################################################
# 
#  Copyright 2019 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

'''
Storage To Table

Move using bucket and path prefix.

S
p
e
c
i
f
y
 
a
 
b
u
c
k
e
t
 
a
n
d
 
p
a
t
h
 
p
r
e
f
i
x
,
 
*
 
s
u
f
f
i
x
 
i
s
 
N
O
T
 
r
e
q
u
i
r
e
d
.


E
v
e
r
y
 
t
i
m
e
 
t
h
e
 
j
o
b
 
r
u
n
s
 
i
t
 
w
i
l
l
 
o
v
e
r
w
r
i
t
e
 
t
h
e
 
t
a
b
l
e
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'bucket': '',  # Google cloud bucket.
  'path': '',  # Path prefix to read from, no * required.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this query.
  'schema': '[]',  # Schema provided in JSON list format or empty list.
}

TASKS = [
  {
    'bigquery': {
      'auth': 'user',
      'from': {
        'bucket': {
          'field': {
            'name': 'bucket',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google cloud bucket.'
          }
        },
        'path': {
          'field': {
            'name': 'path',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Path prefix to read from, no * required.'
          }
        }
      },
      'to': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'table': {
          'field': {
            'name': 'table',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Table to create from this query.'
          }
        }
      },
      'schema': {
        'field': {
          'name': 'schema',
          'kind': 'json',
          'order': 5,
          'default': '[]',
          'description': 'Schema provided in JSON list format or empty list.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_storage', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
