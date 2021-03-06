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
Floodlight Monitor

Monitor floodlight impressions specified in sheet and send email alerts.

S
p
e
c
i
f
y
 
a
n
 
a
c
c
o
u
n
t
_
i
d
 
o
r
 
a
c
c
o
u
n
t
_
i
d
:
s
u
b
a
c
c
o
u
n
t
_
i
d
.


W
i
l
l
 
c
o
p
y
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
d
o
c
s
.
g
o
o
g
l
e
.
c
o
m
/
s
p
r
e
a
d
s
h
e
e
t
s
/
d
/
1
t
j
F
5
s
t
y
x
M
v
F
J
s
N
E
T
E
a
5
x
2
F
5
D
S
m
q
l
e
G
l
7
1
c
m
u
j
B
7
I
e
r
8
/
e
d
i
t
?
u
s
p
=
s
h
a
r
i
n
g
'
>
F
l
o
o
d
l
i
g
h
t
 
M
o
n
i
t
o
r
 
S
h
e
e
t
<
/
a
>
 
t
o
 
t
h
e
 
s
h
e
e
t
 
y
o
u
 
s
p
e
c
i
f
y
.


F
o
l
l
o
w
 
i
n
s
t
r
u
c
t
i
o
n
s
 
o
n
 
s
h
e
e
t
.


E
m
a
i
l
s
 
a
r
e
 
s
e
n
t
 
o
n
c
e
 
a
 
d
a
y
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dcm_account': '',  # Specify an account_id or account_id:subaccount_id.
  'sheet_url': '',  # Full URL to Google Sheet, Floodlight Monitor tab will be added.
}

TASKS = [
  {
    'floodlight_monitor': {
      'auth': 'user',
      'account': {
        'field': {
          'name': 'dcm_account',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'Specify an account_id or account_id:subaccount_id.'
        }
      },
      'template': {
        'template': {
          'sheet': 'https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing',
          'tab': 'Floodlight Monitor',
          'range': 'A1'
        }
      },
      'sheet': {
        'field': {
          'name': 'sheet_url',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Full URL to Google Sheet, Floodlight Monitor tab will be added.'
        }
      },
      'tab': 'Floodlight Monitor',
      'range': 'A2:C'
    }
  }
]

DAG_FACTORY = DAG_Factory('floodlight_monitor', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
