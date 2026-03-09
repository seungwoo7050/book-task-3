#include "inc/debug.hpp"

#include "inc/Message.hpp"

#include <cstdlib>
#include <cstring>
#include <cerrno>
#include <iterator>

namespace debug_csi_params
{
	const std::string clear_screen("\033[2J");
	const std::string carriage_return("\033[H");
	const std::string cursor_up("\033[1A\r");
	const std::string erase_whole_line("\033[2K");
}

namespace debug_sgr_params
{
	const std::string reset("\033[0m");
	const std::string bold_red("\033[1;31m");
	const std::string bold_green("\033[1;32m");
	const std::string bold_yellow("\033[1;33m");
	const std::string bold_blue("\033[0;34m");
	const std::string bold_magenta("\033[1;35m");
	const std::string bold_cyan("\033[1;36m");
	const std::string red("\033[0;31m");
	const std::string green("\033[0;32m");
	const std::string yellow("\033[0;33m");
	const std::string blue("\033[0;34m");
	const std::string magenta("\033[0;35m");
	const std::string cyan("\033[0;36m");
	const std::string gray("\033[0;90m");
	const std::string background_gray("\033[0;100m");
	std::string default_color(reset);
}

static std::string target;

static void _do_leaks()
{
	std::string command = "leaks " + ::target;
	std::cout << std::flush;
	std::system(command.c_str());
}

void debug::check_leaks_atexit(std::string progname)
{
	if (IS_DEFINED(NDEBUG))
		return;
	
	::target = progname.find("./") == 0 ? progname.substr(2) : progname;
	if (std::atexit(_do_leaks) != 0)
	{
		std::cerr
		<< "debug: failed to register an exit hook: leaks"
		<< std::endl;
	}
}

void debug::logl(const std::string &msg, const std::string &color)
{
	if (IS_DEFINED(NDEBUG))
		return;
	
	std::cerr
	<< color
	<< msg
	<< debug_sgr_params::reset
	<< std::endl;
}

void debug::log_recv_status(const int sockfd, const ssize_t bytes, const std::string &packet)
{
	if (IS_DEFINED(NDEBUG))
		return;
	
	static int cnt = 1;
    std::cerr
    << debug_sgr_params::green
    << "< packet #" << cnt++ << " >"
	<< "\n\tsocket fd: " << sockfd
	<< "\n\tbytes read: " << bytes
	<< "\n\terrno: " << std::strerror(errno)
	<< "\n\tpacket size: " << packet.size()
	<< "\n\n\tpacket content:\n"
	<< debug_sgr_params::green
	<< "-----------------------------\n"
	<< packet
	<< "-----------------------------"
    << debug_sgr_params::reset
    << std::endl;
}

void debug::log_send_status(const int sockfd, const ssize_t bytes, const std::string &packet)
{
	if (IS_DEFINED(NDEBUG))
		return;

	static int cnt = 1;
	std::cerr
	<< debug_sgr_params::cyan
	<< "< reply #" << cnt++ << " >"
	<< "\n\treply sent to: " << sockfd
	<< "\n\tbytes written: " << bytes
	<< "\n\terrno: " << std::strerror(errno)
	<< "\n\tpacket size: " << packet.size()
	<< "\n\n\tpacket content:\n"
	<< debug_sgr_params::cyan
	<< "-----------------------------\n"
	<< packet
	<< "-----------------------------"
	<< debug_sgr_params::reset
	<< std::endl;
}

void debug::log_msg_status(const Message &msg)
{
	if (IS_DEFINED(NDEBUG))
		return;

	std::ostream_iterator<std::string> output_iter(std::cerr, "\n");

	std::cerr
	<< debug_sgr_params::yellow
	<< "< parsed message content >"
	<< "\n\tprefix: " << msg.prefix
	<< "\n\tcommand: " << msg.command
	<< "\n\n\tparams: "
	<< "\n-----------------------------\n";
	for (std::vector<std::string>::const_iterator it = msg.params.cbegin(); it != msg.params.cend(); ++it)
	{
		*output_iter++ = *it;
	}
	std::cerr
	<< "-----------------------------"
	<< debug_sgr_params::reset
	<< std::endl;
}
