# Signal And Race Discipline

## Core Race

The classic Shell Lab race is:

1. parent calls `fork`
2. child exits quickly
3. `SIGCHLD` arrives and the handler reaps the child
4. parent tries to add the child to the job list after it is already gone

That leaves the shell's job table inconsistent.

## Required Fix

The shell blocks `SIGCHLD` before `fork`, adds the child to the job list in the parent, and only
then restores the previous mask.

The child restores the old mask before `execvp`.

## Why Process Groups Matter

The shell must not die when the user sends Ctrl-C or Ctrl-Z. It should forward those signals to
the foreground job's process group instead. That is why each child calls `setpgid(0, 0)`.
