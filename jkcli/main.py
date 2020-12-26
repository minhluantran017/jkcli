#!/usr/bin/env python3

import argparse
import logging
import time
import sys
import urllib3
import os
import configparser
import cmd
from os import path
from cli_config import CliConfig
from pipeline import Pipeline

def parse_args():
   parser = argparse.ArgumentParser(
      usage='jenkins-cli <options> <action> ...',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

   # Common parameters

   parser.add_argument('-i', '--instance', type = str, required =False,
                     help = 'The Jenkins master URL')
   parser.add_argument('-u', '--user',     type = str, required =False,
                     help = 'Your Jenkins username')
   parser.add_argument('-p', '--password', type = str, required =False,
                     help = 'Your Jenkins password or API token')
   parser.add_argument(      '--profile',  type = str, required =False,
                     default = 'default',
                     help = 'The Jenkins profile name in Jenkins config file')

   # Sub-command parsers

   subparsers = parser.add_subparsers(help = 'Actions', dest = 'subcommand')

   parser_configure  = subparsers.add_parser('configure',help = 'Configure Jenkins access information')
   parser_validate   = subparsers.add_parser('validate', help = 'Validate a jenkinsfile')
   parser_build      = subparsers.add_parser('build',    help = 'Build a Jenkins job')


   parser_validate.add_argument('-f', '--file',    type = str, required = True,
                              help='The Jenkinsfile to validate')
   
   parser_build.add_argument('-j', '--job',        type = str, required = True,
                           help = 'The Jenkins job name to build')
   parser_build.add_argument(      '--parameters', type = str, required = False,
                           help = 'The Jenkins job parameters to build')
   parser_build.add_argument('-w', '--polling',       
                           dest = 'polling',       action = 'store_true',
                           help = 'Whether wait for job to finish or not')
   parser_build.add_argument('-t', '--timeout',    type = str, required = False,
                           default = '5',
                           help = 'The timeout in minute waiting for job to finish')

   return parser.parse_args()

if __name__ == '__main__':
   args = parse_args()
   logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
               level=logging.DEBUG)
   logger = logging.getLogger(__name__)
   logging.getLogger("urllib3").setLevel(logging.INFO)

   cliConfig = CliConfig(url=args.instance, user=args.user,
                          passwd=args.password, profile = args.profile)

   if args.subcommand == 'configure':
      cliConfig.set_config()

   elif args.subcommand == 'validate':
      creds = cliConfig.get_config()
      pipeline = Pipeline()
      pipeline.validate_jenkinsfile(creds = creds, jenkinsfile=args.file)

   elif args.subcommand == 'build':
      print('TODO')
