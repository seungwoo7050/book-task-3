# Job Control Flow

## Built-ins

The lab really tests four shell-owned actions:

- `quit` exits the shell
- `jobs` shows the job table
- `bg` resumes a stopped job in the background
- `fg` resumes a job in the foreground and then waits for it

## Foreground Waiting

The shell does not wait with a blocking `waitpid` call in the main path. Instead, it waits while
the target PID remains the foreground job, and it lets `SIGCHLD` update the job state.

That is why the shell's signal handlers and the foreground wait loop must agree on the same job
table semantics.
