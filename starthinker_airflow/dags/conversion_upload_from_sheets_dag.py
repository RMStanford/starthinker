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
Conversion Upload Sheets

Move form Sheets to DCM.

S
p
e
c
i
f
y
 
a
 
D
C
M
 
A
c
c
o
u
n
t
 
I
D
,
 
F
l
o
o
d
l
i
g
h
 
A
c
t
i
v
i
t
y
 
I
D
 
a
n
d
 
C
o
n
v
e
r
s
i
o
n
 
T
y
p
e
.


I
n
c
l
u
d
e
 
S
h
e
e
t
s
 
u
r
l
,
 
t
a
b
,
 
a
n
d
 
r
a
n
g
e
,
 
o
m
i
t
 
h
e
a
d
e
r
s
 
i
n
 
r
a
n
g
e
.


C
o
l
u
m
n
s
:
 
O
r
d
i
n
a
l
,
 
t
i
m
e
s
t
a
m
p
M
i
c
r
o
s
,
 
e
n
c
r
y
p
t
e
d
U
s
e
r
I
d
 
|
 
e
n
c
r
y
p
t
e
d
U
s
e
r
I
d
C
a
n
d
i
d
a
t
e
s
 
|
 
g
c
l
i
d
 
|
 
m
o
b
i
l
e
D
e
v
i
c
e
I
d


I
n
c
l
u
d
e
 
e
n
c
r
y
p
t
i
o
n
 
i
n
f
o
r
m
a
t
i
o
n
 
i
f
 
u
s
i
n
g
 
e
n
c
r
y
p
t
e
d
U
s
e
r
I
d
 
o
r
 
e
n
c
r
y
p
t
e
d
U
s
e
r
I
d
C
a
n
d
i
d
a
t
e
s
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dcm_account': '',
  'floodlight_activity_id': '',
  'floodlight_conversion_type': 'encryptedUserId',
  'encryption_entity_id': '',
  'encryption_entity_type': 'DCM_ACCOUNT',
  'encryption_entity_source': 'DATA_TRANSFER',
  'sheet_url': '',
  'sheet_tab': '',
  'sheet_range': '',
}

TASKS = [
  {
    'conversion_upload': {
      'auth': 'user',
      'account_id': {
        'field': {
          'name': 'dcm_account',
          'kind': 'string',
          'order': 0,
          'default': ''
        }
      },
      'activity_id': {
        'field': {
          'name': 'floodlight_activity_id',
          'kind': 'integer',
          'order': 1,
          'default': ''
        }
      },
      'conversion_type': {
        'field': {
          'name': 'floodlight_conversion_type',
          'kind': 'choice',
          'order': 2,
          'choices': [
            'encryptedUserId',
            'encryptedUserIdCandidates',
            'gclid',
            'mobileDeviceId'
          ],
          'default': 'encryptedUserId'
        }
      },
      'encryptionInfo': {
        'encryptionEntityId': {
          'field': {
            'name': 'encryption_entity_id',
            'kind': 'integer',
            'order': 3,
            'default': ''
          }
        },
        'encryptionEntityType': {
          'field': {
            'name': 'encryption_entity_type',
            'kind': 'choice',
            'order': 4,
            'choices': [
              'ADWORDS_CUSTOMER',
              'DBM_ADVERTISER',
              'DBM_PARTNER',
              'DCM_ACCOUNT',
              'DCM_ADVERTISER',
              'ENCRYPTION_ENTITY_TYPE_UNKNOWN'
            ],
            'default': 'DCM_ACCOUNT'
          }
        },
        'encryptionSource': {
          'field': {
            'name': 'encryption_entity_source',
            'kind': 'choice',
            'order': 5,
            'choices': [
              'AD_SERVING',
              'DATA_TRANSFER',
              'ENCRYPTION_SCOPE_UNKNOWN'
            ],
            'default': 'DATA_TRANSFER'
          }
        }
      },
      'sheets': {
        'url': {
          'field': {
            'name': 'sheet_url',
            'kind': 'string',
            'order': 9,
            'default': ''
          }
        },
        'tab': {
          'field': {
            'name': 'sheet_tab',
            'kind': 'string',
            'order': 10,
            'default': ''
          }
        },
        'range': {
          'field': {
            'name': 'sheet_range',
            'kind': 'string',
            'order': 11,
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('conversion_upload_from_sheets', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
