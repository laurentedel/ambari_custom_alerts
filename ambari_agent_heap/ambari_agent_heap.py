#!/usr/bin/env python

import collections
import os
import platform
import sys
from resource_management.core.logger import Logger

MEMORY_USED_WARNING_THRESHOLD  = 1073741824
MEMORY_USED_CRITICAL_THRESHOLD = 3221225472

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return None

def execute(configurations={}, parameters={}, host_name=None):

  p = open("/var/run/ambari-agent/ambari-agent.pid")
  pid=p.read()
  p.close()
  _proc_status = '/proc/%d/status' % int(pid)
  t = open(_proc_status)
  v = t.read()
  t.close()

  i = v.index("VmRSS")
  v = v[i:].split(None, 3)

  memory_used = int(v[1])

  result_code = 'OK'
  if memory_used > MEMORY_USED_CRITICAL_THRESHOLD:
    result_code = 'CRITICAL'
  elif memory_used > MEMORY_USED_WARNING_THRESHOLD:
    result_code = 'WARNING'

  label = 'Memory Used: {0}'.format(_get_formatted_size(memory_used))
  return ((result_code, [label]))

def _get_formatted_size(bytes):
  """
  formats the supplied bytes
  """
  if bytes < 1000:
    return '%i' % bytes + ' b'
  elif 1000 <= bytes < 1000000:
    return '%.1f' % (bytes / 1000.0) + ' Kb'
  elif 1000000 <= bytes < 1000000000:
    return '%.1f' % (bytes / 1000000.0) + ' Mb'
  elif 1000000000 <= bytes < 1000000000000:
    return '%.1f' % (bytes / 1000000000.0) + ' Gb'
  else:
    return '%.1f' % (bytes / 1000000000000.0) + ' Tb'

if __name__ == '__main__':
  execute()
