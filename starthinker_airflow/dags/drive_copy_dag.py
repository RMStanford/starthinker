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
Copy

Copy a drive document.

S
p
e
c
i
f
y
 
a
 
s
o
u
r
c
e
 
U
R
L
 
o
r
 
d
o
c
u
m
e
n
t
 
n
a
m
e
.


S
p
e
c
i
f
y
 
a
 
d
e
s
t
i
n
a
t
i
o
n
 
n
a
m
e
.


I
f
 
d
e
s
t
i
n
a
t
i
o
n
 
d
o
e
s
 
n
o
t
 
e
x
i
s
t
,
 
s
o
u
r
c
e
 
w
i
l
l
 
b
e
 
c
o
p
i
e
d
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'source': '',  # Name or URL of document to copy from.
  'destination': '',  # Name document to copy to.
}

TASKS = [
  {
    'drive': {
      'auth': 'user',
      'copy': {
        'source': {
          'field': {
            'name': 'source',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Name or URL of document to copy from.'
          }
        },
        'destination': {
          'field': {
            'name': 'destination',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name document to copy to.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('drive_copy', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
