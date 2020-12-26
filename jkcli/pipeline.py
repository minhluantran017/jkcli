#!/usr/bin/env python3

import logging
import urllib3
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)

class Pipeline(object):
   def __init__(self):
      return

   def validate_jenkinsfile(self, creds, jenkinsfile):
      http = urllib3.PoolManager()

      crumb_url = '{}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'.format(creds[0])
      header = urllib3.util.make_headers(basic_auth=creds[1]+':'+creds[2])

      crumb_req = http.request('GET', crumb_url, headers=header)
      crumb = crumb_req.data.decode("utf-8")
      
      validate_url = '{}/pipeline-model-converter/validate'.format(creds[0])
      jenkins_file = jenkinsfile if jenkinsfile.startswith("/") else os.getcwd() + "/" + jenkinsfile
      logger.info("Validating {}...".format(jenkins_file))
      with open(jenkins_file) as fp:
         file_data = fp.read()
      validate_req = http.request('POST',validate_url, headers=header, 
                           fields = {'jenkinsfile' : file_data })
      logger.info(validate_req.data.decode("utf-8"))