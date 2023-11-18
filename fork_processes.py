#!/usr/bin/env python3

""" 
    @author Strix Elixel
    @date Nov 17 2023
    @brief Small Processes Library to Fork Processes Easily 
"""

import os
import signal

FORK_ERROR_MESSAGE = "Failed to fork process."
EXEC_ERROR_MESSAGE = "Failed to execute "
FORK_ERROR_CODE = -1
FORK_CHILD_CODE = 0
NOTHING = 0

def error_check_fork(pid):
    if pid == FORK_ERROR_CODE:
        print(FORK_ERROR_MESSAGE)
        os._exit(os.EX_FAILURE)


def is_child(pid):
    error_check_fork(pid)
    return pid == FORK_CHILD_CODE


def handle_exec_fail(program):
    print(EXEC_ERROR_MESSAGE + program)
    os._exit(os.EX_FAILURE)


def execute_program(program, args):
    try:
        os.execvp(program, args)
    except Exception:
        handle_exec_fail(program)


def create_child_program(child_pids, program, args):
    pid = os.fork()
    if is_child(pid):
        execute_program(program, args)
        return NOTHING
    else:  # Parent Process
        child_pids.append(pid)
        return len(child_pids)


def create_child_function(child_pids, execute):
    pid = os.fork()
    if is_child(pid):
        execute()
        os._exit(os.EX_SUCCESS)
    else:  # Parent Process
        child_pids.append(pid)
        return len(child_pids)


def kill_processes(children_processes):
    for child_pid in children_processes:
        print(f"Killing Process ID is {child_pid}")
        os.kill(child_pid, signal.SIGTERM)
    children_processes.clear()


if __name__ == "__main__":
    child_pids = []
    program = "echo"
    args = ["echo", "Hello, World!"]
    create_child_program(child_pids, program, args)
    for _ in range(len(child_pids)):
        os.wait()