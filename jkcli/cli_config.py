#!/usr/bin/env python3

import logging
import time
import os
import configparser

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)

class CliConfig(object):

   def __init__(self, url, user, passwd, profile = 'default'):
      self.url = url
      self.user = user
      self.passwd = passwd
      self.profile = profile

   def read_jenkins_config_param(self):
      '''
      Read Jenkins configuration from direct parameters.
      This takes first priority.
      '''
      if self.url == None or self.user == None or self.passwd == None:
         logger.error("Errors encountered: Missing parameter.")
         raise Exception("Errors encountered: Missing parameter.")
      return [self.url, self.user, self.password]

   def read_jenkins_config_file(self):
      '''
      Read Jenkins configuration from config file.
      The path is in $HOME/.jenkins/config
      This takes second priority.
      '''
      jenkins_profile = 'default' if (self.profile == None) else self.profile
      jenkins_config = configparser.ConfigParser()
      jenkins_config.read('{}/.jenkins/config'.format(os.environ.get('HOME')))
      JENKINS_URL = jenkins_config[jenkins_profile]['JENKINS_URL']
      JENKINS_USER = jenkins_config[jenkins_profile]['JENKINS_USER']
      JENKINS_API_TOKEN = jenkins_config[jenkins_profile]['JENKINS_API_TOKEN']
      return [ JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN ]

   def read_jenkins_config_env(self):
      '''
      Read Jenkins configuration from environment variables.
      This takes third priority.
      '''
      JENKINS_URL = os.environ.get('JENKINS_URL')
      JENKINS_USER = os.environ.get('JENKINS_USER')
      JENKINS_API_TOKEN = os.environ.get('JENKINS_API_TOKEN')
      return [ JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN ]

   def write_jenkins_config_file(self):
      '''
      Write Jenkins configuration to config file.
      The path is in $HOME/.jenkins/config
      '''
      jenkins_url = input("Input Jenkins URL: ")
      jenkins_user = input("Input Jenkins user: ")
      jenkins_token = input("Input Jenkins API token/password: ")
      jenkins_profile = 'default' if (self.profile == None) else self.profile
      jenkins_config = configparser.ConfigParser()
      with open('{}/.jenkins/config'.format(os.environ.get('HOME')), 'r') as config_file:
         jenkins_config.read_file(config_file)
      jenkins_config.remove_section(jenkins_profile)
      jenkins_config[jenkins_profile] = {
         'JENKINS_URL': jenkins_url,
         'JENKINS_USER': jenkins_user,
         'JENKINS_API_TOKEN': jenkins_token
      }
      with open('{}/.jenkins/config'.format(os.environ.get('HOME')), 'w') as config_file:
         jenkins_config.write(config_file)

   def get_config(self):
      '''
      Get Jenkins CLI configuration.
      '''
      logger.info("Getting Jenkins CLI credentials...")

      if (self.url != None) :
         logger.info("Using direct parameters...")
         jenkins_cred = self.read_jenkins_config_param()
      elif os.path.exists("{}/.jenkins/config".format(os.environ.get('HOME'))):
         logger.info("Using config file (~/.jenkins/config)...")
         jenkins_cred = self.read_jenkins_config_file()
      else:
         logger.info("Using environment variables...")
         jenkins_cred = self.read_jenkins_config_env()

      if (jenkins_cred[0] == None):
         logger.error("Errors encountered: Jenkins credentials are not defined.")
         raise Exception("Errors encountered: Jenkins credentials are not defined.")
      else:
         logger.info("Using Jenkins URL: {} with user {}...".format(jenkins_cred[0], jenkins_cred[1]))
         return jenkins_cred

   def set_config(self):
      '''
      Set Jenkins CLI configuration to filesystem.
      '''
      logger.info("Setting Jenkins CLI credentials...")
      self.write_jenkins_config_file()
      logger.info("Succeeded.")
