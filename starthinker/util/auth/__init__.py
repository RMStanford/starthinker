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

import threading

from googleapiclient import discovery

from starthinker.util.project import project
from starthinker.util.auth.wrapper import CredentialsUserWrapper, CredentialsServiceWrapper


CREDENTIALS_USER_CACHE = None # WARNING:  possible issue if switching user credentials mid recipe, not in scope but possible ( need to address using hash? )
DISCOVERY_CACHE = {} 


def clear_credentials_cache():
  global CREDENTIALS_USER_CACHE 
  CREDENTIALS_USER_CACHE = None


def get_credentials(auth):
  global CREDENTIALS_USER_CACHE 

  if auth == 'user':
    if CREDENTIALS_USER_CACHE is None:
      try:
        CREDENTIALS_USER_CACHE = CredentialsUserWrapper(project.recipe['setup']['auth']['user'], project.recipe['setup']['auth'].get('client'))
      except (KeyError, ValueError): 
        raise KeyError("Either specify a -u [user credentials path] parameter on the command line or include setup->auth->user->[JSON OR PATH] in the recipe.")
    return CREDENTIALS_USER_CACHE

  elif auth == 'service':
    try:
      return CredentialsServiceWrapper(project.recipe['setup']['auth']['service'])
    except (KeyError, ValueError): 
      raise KeyError("Either specify a -s [service credentials path] parameter on the command line or include setup->auth->service->[JSON OR PATH] in the recipe.")


def get_service(api='gmail', version='v1', auth='service', scopes=None, uri_file=None):
  global DISCOVERY_CACHE 

  key = api + version + auth + str(threading.current_thread().ident)

  if key not in DISCOVERY_CACHE:
    credentials = get_credentials(auth)
    if uri_file:
      uri_file = uri_file.strip()
      if uri_file.startswith('{'):
        DISCOVERY_CACHE[key] = discovery.build_from_document(uri_file, credentials=credentials)
      else:
        with open(uri_file, 'r') as cache_file:
          DISCOVERY_CACHE[key] = discovery.build_from_document(cache_file.read(), credentials=credentials)
    else:
      DISCOVERY_CACHE[key] = discovery.build(api, version, credentials=credentials)

  return DISCOVERY_CACHE[key]


def get_profile():
  service = get_service('oauth2', 'v2', 'user')
  return service.userinfo().get().execute()


def set_iam(auth, project_id, role, email=None, service=None):
  service = get_service('cloudresourcemanager', 'v1', auth, ['https://www.googleapis.com/auth/cloud-platform'])
  policy = service.projects().getIamPolicy(resource=project_id, body={}).execute()

  if email: member = 'user:%s' % email
  elif service: member = 'service:%s' % service
  else: member = None

  if member:
    for r in policy['bindings']:
      if r['role'] == role and member not in r['members']:
        if project.verbose: print('Settings Role:', member, role)
        r['members'].append(member)
        policy = service.projects().setIamPolicy(resource=project_id, body={ "policy":policy }).execute()
