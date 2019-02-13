#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# Throws an alert regarding the threads CPU consumption
#
# Laurent Edel <ledel@hortonworks.com>
#

import os
import logging
import subprocess

RESULT_STATE_OK       = 'OK'
RESULT_STATE_WARNING  = 'WARNING'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_UNKNOWN  = 'UNKNOWN'

HIVE_PID_DIR          = '{{hive-env/hive_pid_dir}}'

THRESHOLD_WARN        = 'thread_cpu.threshold.warning'
THRESHOLD_CRITICAL    = 'thread_cpu.threshold.critical'
ITERATIONS            = 'thread_cpu.iterations'

logger = logging.getLogger()

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (HIVE_PID_DIR, THRESHOLD_WARN, THRESHOLD_CRITICAL, ITERATIONS)


def execute(configurations={}, parameters={}, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  configurations (dictionary): a mapping of configuration key to value
  parameters (dictionary): a mapping of script parameter key to value
  host_name (string): the name of this host where the alert is running

  """

  # Check required properties
  if configurations is None:
    return (RESULT_STATE_UNKNOWN, ['There were no configurations supplied to the script.'])

  if HIVE_PID_DIR not in configurations:
    return (RESULT_STATE_UNKNOWN, ['{0} is a required parameter for the script'.format(HIVE_PID_DIR)])

  hive_pid_dir = configurations[HIVE_PID_DIR]

  if hive_pid_dir is None:
    return (RESULT_STATE_UNKNOWN, ['{0} is a required parameter for the script and the value is null'.format(HIVE_PID_DIR)])


  if THRESHOLD_WARN in parameters:
    warn_threshold = float(parameters[THRESHOLD_WARN])

  if THRESHOLD_CRITICAL in parameters:
    critical_threshold = float(parameters[THRESHOLD_CRITICAL])

  if ITERATIONS in parameters:
    iterations = str(parameters[ITERATIONS]).split('.')[0]

  messages = []
  perf_ok = set()
  perf_warning = set()
  perf_critical = set()

  o = subprocess.check_output(["bash","-c", "top -H -p $(cat " + hive_pid_dir + "/hive-server.pid) -b -n" + str(int(iterations)) + " | awk '$9 > 0 {print $1,$9}' | grep '^[0-9]' | awk '{a[$1] += $2; b[$1] += 1} END{for (i in a) print i, a[i]/b[i]}' | awk '$2 > " + str(int(warn_threshold)) + " {print $1,$2}'"],stderr=subprocess.STDOUT)

  if o.count("\n") > 0:
    for thread in o.split("\n"):
      if thread.split(" ")[1] > critical_threshold:
        perf_critical.add("thread " + thread.split(" ")[0] + " (" + thread.split(" ")[1] + "%CPU")
      elif thread.split(" ")[1] > warn_threshold:
        perf_warning.add("thread " + thread.split(" ")[0] + " (" + thread.split(" ")[1] + "%CPU")

  status = RESULT_STATE_UNKNOWN

  if not(perf_ok):
    status = RESULT_STATE_OK
    messages.append("Threads CPU consumption is OK")
  if len(perf_warning) > 0:
    status = RESULT_STATE_WARNING
    messages.append("Threads CPU consumption is more than " + str(performance_warn_threshold) + "%: {0}".format(", ".join(perf_warning)))
  if len(perf_critical) > 0:
    status = RESULT_STATE_CRITICAL
    messages.append("Threads CPU consumption is more than " + str(performance_critical_threshold) + "%: {0}".format(", ".join(perf_critical)))

  return (status, [messages])
