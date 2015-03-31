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
import os
import sys
import subprocess


# TAU modules
import logger
import settings
import error
import controller
import util
import environment
import cf.tau
import cf.pdt
from model.project import Project
from model.target import Target
from model.compiler import Compiler

LOGGER = logger.getLogger(__name__)


class Experiment(controller.Controller):
  """
  Experiment data model controller
  """
  
  attributes = {
    'project': {
      'model': 'Project',
      'required': True,
    },
    'target': {
      'model': 'Target',
      'required': True,
    },
    'application': {
      'model': 'Application',
      'required': True,
    },
    'measurement': {
      'model': 'Measurement',
      'required': True,
    },
    'trials': {
      'collection': 'Trial',
      'via': 'experiment'
    },
  }
  
  def onDelete(self):
    if self.isSelected():
      settings.unset('experiment_id')

  def select(self):
    if not self.eid:
      raise error.InternalError('Tried to select an experiment without an eid')
    settings.set('experiment_id', self.eid)
  
  def isSelected(self):
    if self.eid:
      return settings.get('experiment_id') == self.eid
    return False

  @classmethod
  def getSelected(cls):
    experiment_id = settings.get('experiment_id')
    if experiment_id:
      found = cls.one(eid=experiment_id)
      if not found:
        raise error.InternalError('Invalid experiment ID: %r' % experiment_id)
      return found
    return None

  def configure(self):
    """
    Installs all software required to perform the experiment
    """
    self.populate()
    target = self['target']
    application = self['application']
    measurement = self['measurement']
    target.populate()
    cc = target['CC']
    cxx = target['CXX']
    fc = target['FC']
    verbose = (logger.LOG_LEVEL == 'DEBUG')

    # Make sure project prefix exists
    prefix = self['project']['prefix']
    try:
      util.mkdirp(prefix)
    except:
      raise error.ConfigurationError('Cannot create directory %r' % prefix, 
                                     'Check that you have `write` access')

    # Configure/build/install PDT if needed
    if not measurement['source_inst']:
      self.pdt = None
    else:
      pdt = cf.pdt.Pdt(prefix, cxx, target['pdt_source'], target['host_arch'])
      pdt.install()
      self.pdt = pdt
      
    # Configure/build/install TAU if needed
    tau = cf.tau.Tau(prefix, cc, cxx, fc, target['tau_source'], target['host_arch'],
                     verbose=verbose,
                     pdt=pdt,
                     bfd=None, # TODO
                     libunwind=None, # TODO
                     profile=measurement['profile'],
                     trace=measurement['trace'],
                     sample=measurement['sample'],
                     source_inst=measurement['source_inst'],
                     compiler_inst=measurement['compiler_inst'],
                     # TODO: Library wrapping inst
                     openmp_support=application['openmp'], 
                     openmp_measurements=measurement['openmp'],
                     pthreads_support=application['pthreads'], 
                     pthreads_measurements=None, # TODO
                     mpi_support=application['mpi'], 
                     mpi_measurements=measurement['mpi'],
                     cuda_support=application['cuda'],
                     cuda_measurements=None, # Todo
                     shmem_support=application['shmem'],
                     shmem_measurements=None, # TODO
                     mpc_support=application['mpc'],
                     mpc_measurements=None, # TODO
                     memory_support=None, # TODO
                     memory_measurements=None, # TODO
                     callpath=measurement['callpath'])
    tau.install()
    self.tau = tau

  def managedBuild(self, compiler_cmd, compiler_args):
    """
    TODO: Docs
    """
    self.configure()
    target = self['target']
    measurement = self['measurement']
    given_compiler = Compiler.identify(compiler_cmd)
    target_compiler = target[given_compiler['role']]
    
    # Confirm target supports compiler
    if given_compiler.eid != target_compiler.eid:
      raise error.ConfigurationError("Target '%s' is configured with %s compiler '%s', not '%s'",
                                     (self['name'], given_compiler['language'], 
                                      given_compiler.absolutePath(),
                                      target_compiler.absolutePath()),
                                     "Use a different target or use compiler '%s'" %
                                     target_compiler.absolutePath())

    # Build compile-time environment from component packages
    opts, env = [], os.environ
    if measurement['source_inst']:
      self.pdt.applyCompiletimeConfig(opts, env)
    self.tau.applyCompiletimeConfig(opts, env)

    use_wrapper = measurement['source_inst'] or measurement['comp_inst']
    if use_wrapper:
      compiler_cmd = given_compiler['tau_wrapper']

    cmd = [compiler_cmd] + opts + compiler_args

    LOGGER.debug('Creating subprocess: cmd=%r, env=%r' % (cmd, env))
    LOGGER.info('\n'.join(['%s=%s' % i for i in env.iteritems() if i[0].startswith('TAU')]))
    LOGGER.info(' '.join(cmd))
    with logger.logging_streams():
      proc = subprocess.Popen(cmd, env=env, stdout=sys.stdout, stderr=sys.stderr)
      return proc.wait()

  @classmethod
  def managedRun(cls, selection, application_cmd, application_args):
    """
    TODO: Docs
    """
    selection.populate()
    target = selection['target']
    application = selection['application']
    measurement = selection['measurement']

    expr = cls.configure(selection, cc, cxx, fc)
    opts, env = expr.getCompiletimeConfig()

    use_wrapper = measurement['source_inst'] or measurement['comp_inst']
    if use_wrapper:
      compiler_cmd = key_compiler['tau_wrapper']

    cmd = [compiler_cmd] + opts + compiler_args

    LOGGER.debug('Creating subprocess: cmd=%r, env=%r' % (cmd, env))
    LOGGER.info('\n'.join(['%s=%s' % i for i in env.iteritems() if i[0].startswith('TAU')]))
    LOGGER.info(' '.join(cmd))
    with logger.logging_streams():
      proc = subprocess.Popen(cmd, env=env, stdout=sys.stdout, stderr=sys.stderr)
      return proc.wait()
