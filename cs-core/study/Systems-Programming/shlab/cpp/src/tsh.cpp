#include <cctype>
#include <cerrno>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include "tsh_helper.hpp"

#define MAXLINE 1024
#define MAXARGS 128
#define MAXJOBS 16

#define UNDEF 0
#define FG 1
#define BG 2
#define ST 3

extern char **environ;

static char prompt[] = "tsh> ";
static int verbose = 0;

struct job_t {
    pid_t pid;
    int jid;
    int state;
    char cmdline[MAXLINE];
};

static job_t jobs[MAXJOBS];
static int nextjid = 1;

using handler_t = void(int);

static void eval(char *cmdline);
static int builtin_cmd(char **argv);
static void do_bgfg(char **argv);
static void waitfg(pid_t pid);
static void sigchld_handler(int sig);
static void sigint_handler(int sig);
static void sigtstp_handler(int sig);

static int parseline(const char *cmdline, char **argv);
static void clearjob(job_t *job);
static void initjobs(job_t *jlist);
static int addjob(job_t *jlist, pid_t pid, int state, const char *cmdline);
static int deletejob(job_t *jlist, pid_t pid);
static pid_t fgpid(job_t *jlist);
static job_t *getjobpid(job_t *jlist, pid_t pid);
static job_t *getjobjid(job_t *jlist, int jid);
static int pid2jid(pid_t pid);
static void listjobs(job_t *jlist);
static void usage(void);
static void unix_error(const char *msg);
static void app_error(const char *msg);
static handler_t *Signal(int signum, handler_t *handler);

int main(int argc, char **argv)
{
    char cmdline[MAXLINE];
    int emit_prompt = 1;
    int c;

    opterr = 0;
    while ((c = getopt(argc, argv, "hvp")) != EOF) {
        switch (c) {
        case 'h':
            usage();
            break;
        case 'v':
            verbose = 1;
            break;
        case 'p':
            emit_prompt = 0;
            break;
        default:
            usage();
        }
    }

    Signal(SIGINT, sigint_handler);
    Signal(SIGTSTP, sigtstp_handler);
    Signal(SIGCHLD, sigchld_handler);
    initjobs(jobs);

    while (1) {
        if (emit_prompt) {
            std::printf("%s", prompt);
            std::fflush(stdout);
        }
        if (std::fgets(cmdline, MAXLINE, stdin) == nullptr) {
            if (std::ferror(stdin)) {
                app_error("fgets error");
            }
            std::exit(0);
        }
        eval(cmdline);
        std::fflush(stdout);
    }
}

static void eval(char *cmdline)
{
    char *argv[MAXARGS];
    const int bg = parseline(cmdline, argv);
    pid_t pid;
    sigset_t mask_child;
    sigset_t mask_all;
    sigset_t prev;

    if (argv[0] == nullptr) {
        return;
    }
    if (builtin_cmd(argv)) {
        return;
    }

    sigemptyset(&mask_child);
    sigaddset(&mask_child, SIGCHLD);
    sigfillset(&mask_all);

    if (sigprocmask(SIG_BLOCK, &mask_child, &prev) < 0) {
        unix_error("sigprocmask error");
    }

    pid = fork();
    if (pid < 0) {
        unix_error("fork error");
    }

    if (pid == 0) {
        if (sigprocmask(SIG_SETMASK, &prev, nullptr) < 0) {
            _exit(1);
        }
        if (setpgid(0, 0) < 0) {
            _exit(1);
        }
        execvp(argv[0], argv);
        std::printf("%s: Command not found\n", argv[0]);
        _exit(1);
    }

    if (sigprocmask(SIG_BLOCK, &mask_all, nullptr) < 0) {
        unix_error("sigprocmask error");
    }
    addjob(jobs, pid, bg ? BG : FG, cmdline);
    if (sigprocmask(SIG_SETMASK, &prev, nullptr) < 0) {
        unix_error("sigprocmask error");
    }

    if (!bg) {
        waitfg(pid);
    } else {
        std::printf("[%d] (%d) %s", pid2jid(pid), pid, cmdline);
    }
}

static int builtin_cmd(char **argv)
{
    if (std::strcmp(argv[0], "quit") == 0) {
        std::exit(0);
    }
    if (std::strcmp(argv[0], "jobs") == 0) {
        listjobs(jobs);
        return 1;
    }
    if (std::strcmp(argv[0], "bg") == 0 || std::strcmp(argv[0], "fg") == 0) {
        do_bgfg(argv);
        return 1;
    }
    return 0;
}

static void do_bgfg(char **argv)
{
    job_t *job = nullptr;
    int id;

    if (argv[1] == nullptr) {
        std::printf("%s command requires PID or %%jobid argument\n", argv[0]);
        return;
    }

    if (argv[1][0] == '%') {
        id = std::atoi(&argv[1][1]);
        job = getjobjid(jobs, id);
        if (job == nullptr) {
            std::printf("%%%d: No such job\n", id);
            return;
        }
    } else if (std::isdigit(static_cast<unsigned char>(argv[1][0]))) {
        id = std::atoi(argv[1]);
        job = getjobpid(jobs, static_cast<pid_t>(id));
        if (job == nullptr) {
            std::printf("(%d): No such process\n", id);
            return;
        }
    } else {
        std::printf("%s: argument must be a PID or %%jobid\n", argv[0]);
        return;
    }

    if (kill(-job->pid, SIGCONT) < 0) {
        unix_error("kill (SIGCONT) error");
    }

    if (std::strcmp(argv[0], "fg") == 0) {
        job->state = FG;
        waitfg(job->pid);
    } else {
        job->state = BG;
        std::printf("[%d] (%d) %s", job->jid, job->pid, job->cmdline);
    }
}

static void waitfg(pid_t pid)
{
    sigset_t empty;
    sigemptyset(&empty);
    while (fgpid(jobs) == pid) {
        sigsuspend(&empty);
    }
}

static void sigchld_handler(int sig)
{
    int olderrno = errno;
    int status;
    pid_t pid;

    (void)sig;

    while ((pid = waitpid(-1, &status, WNOHANG | WUNTRACED)) > 0) {
        if (WIFEXITED(status)) {
            deletejob(jobs, pid);
        } else if (WIFSIGNALED(status)) {
            int jid = pid2jid(pid);
            sio_puts("Job [");
            sio_putl(jid);
            sio_puts("] (");
            sio_putl(pid);
            sio_puts(") terminated by signal ");
            sio_putl(WTERMSIG(status));
            sio_puts("\n");
            deletejob(jobs, pid);
        } else if (WIFSTOPPED(status)) {
            job_t *job = getjobpid(jobs, pid);
            if (job != nullptr) {
                job->state = ST;
                sio_puts("Job [");
                sio_putl(job->jid);
                sio_puts("] (");
                sio_putl(pid);
                sio_puts(") stopped by signal ");
                sio_putl(WSTOPSIG(status));
                sio_puts("\n");
            }
        }
    }

    errno = olderrno;
}

static void sigint_handler(int sig)
{
    const int olderrno = errno;
    const pid_t pid = fgpid(jobs);
    if (pid > 0) {
        kill(-pid, sig);
    }
    errno = olderrno;
}

static void sigtstp_handler(int sig)
{
    const int olderrno = errno;
    const pid_t pid = fgpid(jobs);
    if (pid > 0) {
        kill(-pid, sig);
    }
    errno = olderrno;
}

static int parseline(const char *cmdline, char **argv)
{
    static char array[MAXLINE];
    char *buf = array;
    char *delim;
    int argc = 0;
    int bg;

    std::strcpy(buf, cmdline);
    buf[std::strlen(buf) - 1] = ' ';

    while (*buf && (*buf == ' ')) {
        buf++;
    }

    while ((delim = std::strchr(buf, ' '))) {
        argv[argc++] = buf;
        *delim = '\0';
        buf = delim + 1;
        while (*buf && (*buf == ' ')) {
            buf++;
        }
    }
    argv[argc] = nullptr;

    if (argc == 0) {
        return 1;
    }

    bg = (*argv[argc - 1] == '&');
    if (bg) {
        argv[--argc] = nullptr;
    }
    return bg;
}

static void clearjob(job_t *job)
{
    job->pid = 0;
    job->jid = 0;
    job->state = UNDEF;
    job->cmdline[0] = '\0';
}

static void initjobs(job_t *jlist)
{
    for (int i = 0; i < MAXJOBS; i++) {
        clearjob(&jlist[i]);
    }
}

static int addjob(job_t *jlist, pid_t pid, int state, const char *cmdline)
{
    if (pid < 1) {
        return 0;
    }
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].pid == 0) {
            jlist[i].pid = pid;
            jlist[i].state = state;
            jlist[i].jid = nextjid++;
            if (nextjid > MAXJOBS) {
                nextjid = 1;
            }
            std::strcpy(jlist[i].cmdline, cmdline);
            if (verbose) {
                std::printf("Added job [%d] %d %s\n", jlist[i].jid, pid, cmdline);
            }
            return 1;
        }
    }
    std::printf("Tried to create too many jobs\n");
    return 0;
}

static int deletejob(job_t *jlist, pid_t pid)
{
    if (pid < 1) {
        return 0;
    }
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].pid == pid) {
            clearjob(&jlist[i]);
            nextjid = 1;
            for (int j = 0; j < MAXJOBS; j++) {
                if (jlist[j].jid > nextjid) {
                    nextjid = jlist[j].jid;
                }
            }
            nextjid++;
            return 1;
        }
    }
    return 0;
}

static pid_t fgpid(job_t *jlist)
{
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].state == FG) {
            return jlist[i].pid;
        }
    }
    return 0;
}

static job_t *getjobpid(job_t *jlist, pid_t pid)
{
    if (pid < 1) {
        return nullptr;
    }
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].pid == pid) {
            return &jlist[i];
        }
    }
    return nullptr;
}

static job_t *getjobjid(job_t *jlist, int jid)
{
    if (jid < 1) {
        return nullptr;
    }
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].jid == jid) {
            return &jlist[i];
        }
    }
    return nullptr;
}

static int pid2jid(pid_t pid)
{
    if (pid < 1) {
        return 0;
    }
    for (int i = 0; i < MAXJOBS; i++) {
        if (jobs[i].pid == pid) {
            return jobs[i].jid;
        }
    }
    return 0;
}

static void listjobs(job_t *jlist)
{
    for (int i = 0; i < MAXJOBS; i++) {
        if (jlist[i].pid != 0) {
            std::printf("[%d] (%d) ", jlist[i].jid, jlist[i].pid);
            switch (jlist[i].state) {
            case BG:
                std::printf("Running ");
                break;
            case FG:
                std::printf("Foreground ");
                break;
            case ST:
                std::printf("Stopped ");
                break;
            default:
                std::printf("Internal error ");
                break;
            }
            std::printf("%s", jlist[i].cmdline);
        }
    }
}

static void usage(void)
{
    std::printf("Usage: tsh [-hvp]\n");
    std::printf("   -h   print this message\n");
    std::printf("   -v   verbose\n");
    std::printf("   -p   no prompt\n");
    std::exit(1);
}

static void unix_error(const char *msg)
{
    std::fprintf(stdout, "%s: %s\n", msg, std::strerror(errno));
    std::exit(1);
}

static void app_error(const char *msg)
{
    std::fprintf(stdout, "%s\n", msg);
    std::exit(1);
}

static handler_t *Signal(int signum, handler_t *handler)
{
    struct sigaction action;
    struct sigaction old_action;

    action.sa_handler = handler;
    sigemptyset(&action.sa_mask);
    action.sa_flags = SA_RESTART;

    if (sigaction(signum, &action, &old_action) < 0) {
        unix_error("Signal error");
    }
    return old_action.sa_handler;
}
