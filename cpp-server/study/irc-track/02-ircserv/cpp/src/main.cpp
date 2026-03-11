#include "inc/EventManager.hpp"
#include "inc/Server.hpp"
#include "inc/debug.hpp"

#include <signal.h>
#include <cstring>
#include <cerrno>

int main(int ac, char *av[])
{
	debug::check_leaks_atexit(av[0]);

	if (ac != 3)
	{
		std::cerr << "usage: " << av[0] << " <port> <password>" << std::endl;
		return 1;
	}

	struct sigaction act;
	std::memset(&act, 0, sizeof(act));
	act.sa_handler = SIG_IGN;

#if defined(__linux__)
	sigset_t mask;
	std::memset(&mask, 0, sizeof(mask));
	sigemptyset(&mask);
	sigaddset(&mask, SIGINT);
	if (sigprocmask(SIG_BLOCK, &mask, NULL) == -1)
	{
		std::cerr << "fatal: sigprocmask: " << std::strerror(errno) << std::endl;
		return 1;
	}
#endif

	if (sigaction(SIGPIPE, &act, NULL) == -1
		|| sigaction(SIGQUIT, &act, NULL) == -1
		|| sigaction(SIGTSTP, &act, NULL) == -1
#if defined(__APPLE__)
		|| sigaction(SIGINT, &act, NULL) == -1
#endif
		)
	{
		std::cerr << "fatal: sigaction: " << std::strerror(errno) << std::endl;
		return 1;
	}

	try
	{
		Server server(av[1], av[2]);
		server.run();
	}
	catch(const std::invalid_argument &e)
	{
		std::cerr << av[0] << ": " << e.what() << std::endl;
		return 1;
	}
	catch(const std::exception &e)
	{
		std::cerr << av[0] << ": fatal: " << e.what() << std::strerror(errno) << std::endl;
		return 1;
	}
}
