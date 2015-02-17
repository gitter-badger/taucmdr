"""
@file
@author John C. Linford (jlinford@paratools.com)
@version 1.0

@brief

This file is part of the TAU Performance System

@section COPYRIGHT

Copyright (c) 2013, ParaTools, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:
 (1) Redistributions of source code must retain the above copyright notice, 
     this list of conditions and the following disclaimer.
 (2) Redistributions in binary form must reproduce the above copyright notice, 
     this list of conditions and the following disclaimer in the documentation 
     and/or other materials provided with the distribution.
 (3) Neither the name of ParaTools, Inc. nor the names of its contributors may 
     be used to endorse or promote products derived from this software without 
     specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# System modules
from texttable import Texttable

# TAU modules
from tau import USER_PREFIX, EXIT_SUCCESS
from logger import getLogger, LINE_WIDTH
from util import pformatList, pformatDict
from error import ConfigurationError
from arguments import getParser, SUPPRESS
from texttable import Texttable
from api.target import Target


LOGGER = getLogger(__name__)

SHORT_DESCRIPTION = "List target configurations or show configuration details."

COMMAND = ' '.join(['tau'] + (__name__.split('.')[1:]))

USAGE = """
Usage:
  %(command)s [target_name] [target_name] ...
  %(command)s -h | --help
"""

HELP = """
'%(command)s' page to be written.
""" % {'command': COMMAND}

_arguments = [(('names',), {'help': "If given, show only targets with this name",
                           'metavar': 'target_name', 
                           'nargs': '*',
                           'default': SUPPRESS})]
PARSER = getParser(_arguments,
                   prog=COMMAND, 
                   usage=USAGE % {'command': COMMAND}, 
                   description=SHORT_DESCRIPTION)


def getUsage():
  return PARSER.format_help() 


def getHelp():
  return HELP

def main(argv):
  """
  Program entry point
  """ 
  args = PARSER.parse_args(args=argv)
  LOGGER.debug('Arguments: %s' % args)
  
  try:
    names = args.names
  except AttributeError:
    found = Target.search()
  else:
    found = []
    for name in names:
      t = Target.withName(name)
      if t:
        found.append(t)

  title = '{:=<75}'.format('== Targets (%s) ==' % USER_PREFIX)
  if not found:
    listing = "No targets. See 'tau target create --help'"
  else:
    table = Texttable(LINE_WIDTH)
    cols = [('Name', 'r', 'name'), 
            ('Host OS', 'c', 'host_os'), 
            ('Host Arch.', 'c', 'host_arch'), 
            ('Device Arch.', 'c', 'device_arch'),
            ('In Projects', 'l', None)]
    headers = [header for header, _, _ in cols]
    rows = [headers]
    for t in found:
      t.populate()
      projects = ', '.join([p['name'] for p in t['projects']])
      row = [t.get(attr, None) for _, _, attr in cols if attr] + [projects]
      rows.append(row)
    table.set_cols_align([align for _, align, _ in cols])
    table.add_rows(rows)
    listing = table.draw()
    
  LOGGER.info('\n'.join([title, '', listing, '']))
  return EXIT_SUCCESS
