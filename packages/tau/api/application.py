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
import string

# TAU modules
from logger import getLogger
from model import Model, ModelError, ByName
from arguments import ParseBooleanAction


LOGGER = getLogger(__name__)


class Application(Model, ByName):
  """
  Application data model
  """
  
  model_name = 'Application'
  
  attributes = {
    'projects': {
      'collection': 'Project',
      'via': 'applications'
    },
    'name': {
      'type': 'string',
      'unique': True,
      'argparse': (('name',), 
                   {'help': 'Application configuration name',
                    'metavar': '<application_name>'})

    },
    'version': {
      'type': 'string',
      'argparse': (('--version',), 
                   {'help': 'Application version',
                    'metavar': '<version>'})
    },
    'source': {
      'type': 'binary',
      'argparse': (('--source',), {'help': 'Application source code',
                                   'metavar': '<source>'})
    },
    'repo': {
      'type': 'string',
      'argparse': (('--repo',), 
                   {'help': 'Application repository',
                    'metavar': '<repo>'})
    },
    'openmp': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--openmp',), 
                   {'help': 'The application uses OpenMP',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    },
    'pthreads': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--pthreads',), 
                   {'help': 'The application uses pthreads',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    },
    'mpi': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--mpi',), 
                   {'help': 'The application uses MPI',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    },
    'cuda': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--cuda',), 
                   {'help': 'The application uses NVIDIA CUDA',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    },
    'shmem': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--shmem',), 
                   {'help': 'The application uses SHMEM',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    },
    'mpc': {
      'type': 'boolean',
      'defaultsTo': False,
      'argparse': (('--mpc',), 
                   {'help': 'The application uses MPC',
                    'metavar': '<flag>',
                    'nargs': '?',
                    'const': True,
                    'default': False,
                    'action': ParseBooleanAction})
    }
  }
  
  _valid_name = set(string.digits + string.letters + '-_.')
  
  def onCreate(self):
    if set(self['name']) > Application._valid_name:
      raise ModelError('%r is not a valid application name.' % self['name'],
                       'Use only letters, numbers, dot (.), dash (-), and underscore (_).')

