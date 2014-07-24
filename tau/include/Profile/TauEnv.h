/****************************************************************************
**			TAU Portable Profiling Package                     **
**			http://www.cs.uoregon.edu/research/tau             **
*****************************************************************************
**    Copyright 2008  						   	   **
**    Department of Computer and Information Science, University of Oregon **
**    Advanced Computing Laboratory, Los Alamos National Laboratory        **
**    Forschungszentrum Juelich                                            **
****************************************************************************/
/****************************************************************************
**	File 		: TauEnv.h 			        	   **
**	Description 	: TAU Profiling Package				   **
**	Author		: Alan Morris					   **
**	Contact		: tau-bugs@cs.uoregon.edu               	   **
**	Documentation	: See http://www.cs.uoregon.edu/research/tau       **
**                                                                         **
**      Description     : Handle environment variables                     **
**                                                                         **
****************************************************************************/

#ifndef _TAU_ENV_H_
#define _TAU_ENV_H_

#include <tau_internal.h>

#define TAU_FORMAT_PROFILE 1
#define TAU_FORMAT_SNAPSHOT 2
#define TAU_FORMAT_MERGED 3
#define TAU_FORMAT_NONE 4
#define TAU_MAX_RECORDS 64*1024

#define TAU_ACTION_DUMP_PROFILES 1
#define TAU_ACTION_DUMP_CALLPATHS 2
#define TAU_ACTION_DUMP_BACKTRACES 3

#ifndef TAU_EVENT_THRESHOLD
#define TAU_EVENT_THRESHOLD_DEFAULT .5
#endif /* TAU_EVENT_THRESHOLD */

#ifdef __cplusplus
extern "C" {
#endif
  
  void TAU_VERBOSE(const char *format, ...);

  void TAUDECL TauEnv_initialize();
  int  TAUDECL TauEnv_get_synchronize_clocks();
  int  TAUDECL TauEnv_get_verbose();
  int  TAUDECL TauEnv_get_throttle();
  int  TAUDECL TauEnv_get_profiling();
  int  TAUDECL TauEnv_get_tracing();
  int  TAUDECL TauEnv_get_callpath();
  int  TAUDECL TauEnv_get_callpath_depth();
  int  TAUDECL TauEnv_get_callsite();
  int  TAUDECL TauEnv_get_callsite_limit();
  int  TAUDECL TauEnv_get_depth_limit();
  void TAUDECL TauEnv_set_depth_limit(int value);
  int  TAUDECL TauEnv_get_comm_matrix();
  int  TAUDECL TauEnv_get_track_message();
  int  TAUDECL TauEnv_get_lite_enabled();
  int  TAUDECL TauEnv_get_compensate();
  int  TAUDECL TauEnv_get_track_memory_heap();
  int  TAUDECL TauEnv_get_track_memory_leaks();
  int  TAUDECL TauEnv_get_track_memory_headroom();
  int  TAUDECL TauEnv_get_track_io_params();
  int  TAUDECL TauEnv_get_track_signals();
  int  TAUDECL TauEnv_get_signals_gdb();
  int  TAUDECL TauEnv_get_openmp_runtime_enabled();
  int  TAUDECL TauEnv_get_openmp_runtime_context();
  int  TAUDECL TauEnv_get_openmp_runtime_states_enabled();
  int  TAUDECL TauEnv_get_openmp_runtime_events_enabled();
  int  TAUDECL TauEnv_get_ebs_enabled();
  int  TAUDECL TauEnv_get_ebs_enabled_tau();
  int  TAUDECL TauEnv_get_ebs_keep_unresolved_addr();
  void  TAUDECL TauEnv_force_set_ebs_period(int period);
  int  TAUDECL TauEnv_get_ebs_period();
  int  TAUDECL TauEnv_get_ebs_inclusive();
  char *  TAUDECL Tau_check_dirname(const char *dirname);
  int  TAUDECL TauEnv_get_ebs_unwind();
  int  TAUDECL TauEnv_get_ebs_unwind_depth();
  int  TAUDECL TauEnv_get_stat_precompute();
  int  TAUDECL TauEnv_get_child_forkdirs();
  int  TAUDECL TauEnv_get_summary_only();
  int  TAUDECL TauEnv_get_ibm_bg_hwp_counters();
  double TAUDECL TauEnv_get_max_records(); 
  double TAUDECL TauEnv_get_evt_threshold(); 
  int TAUDECL TauEnv_get_disable_instrumentation(); 

  const char* TAUDECL TauEnv_get_ebs_source();
  void TAUDECL TauEnv_override_ebs_source(const char *newName);
  double      TAUDECL TauEnv_get_throttle_numcalls();
  double      TAUDECL TauEnv_get_throttle_percall();
  const char* TAUDECL TauEnv_get_profiledir();
  const char* TAUDECL TauEnv_get_tracedir();
  const char* TAUDECL TauEnv_get_metrics();
  const char* TAUDECL TauEnv_get_cupti_api();
  const char* TAUDECL TauEnv_get_cuda_instructions();
  int TAUDECL TauEnv_get_cuda_track_cdp();
  int TAUDECL TauEnv_get_mic_offload();
  int TAUDECL TauEnv_get_bfd_lookup();

  int  TAUDECL TauEnv_get_profile_format();
  int  TAUDECL TauEnv_get_sigusr1_action();
  
  int TAUDECL TauEnv_get_memdbg();
  int TAUDECL TauEnv_get_memdbg_protect_above();
  int TAUDECL TauEnv_get_memdbg_protect_below();
  int TAUDECL TauEnv_get_memdbg_protect_free();
  int TAUDECL TauEnv_get_memdbg_protect_gap();
  int TAUDECL TauEnv_get_memdbg_fill_gap();
  unsigned char TAUDECL TauEnv_get_memdbg_fill_gap_value();
  int TAUDECL TauEnv_get_memdbg_alloc_min();
  size_t TAUDECL TauEnv_get_memdbg_alloc_min_value();
  int TAUDECL TauEnv_get_memdbg_alloc_max();
  size_t TAUDECL TauEnv_get_memdbg_alloc_max_value();
  int TAUDECL TauEnv_get_memdbg_overhead();
  size_t TAUDECL TauEnv_get_memdbg_overhead_value();
  size_t TAUDECL TauEnv_get_memdbg_alignment();
  int TAUDECL TauEnv_get_memdbg_zero_malloc();
  int TAUDECL TauEnv_get_memdbg_attempt_continue();
  int TAUDECL TauEnv_get_pthread_stack_size();
  int TAUDECL TauEnv_get_alfred_port();

#ifdef __cplusplus
}
#endif


#endif /* _TAU_ENV_H_ */