#pragma once

#define STRINGIFY(x) ""#x	// 빈 문자열도 처리한다.
#define IS_DEFINED(MACRO) (__builtin_strcmp(""#MACRO, STRINGIFY(MACRO)))

#include <string>
#include <iostream>

namespace debug_csi_params
{
	extern const std::string clear_screen;
	extern const std::string carriage_return;
	extern const std::string cursor_up;
}

namespace debug_sgr_params
{
	extern const std::string reset;
	extern const std::string bold_red;
	extern const std::string bold_green;
	extern const std::string bold_yellow;
	extern const std::string bold_blue;
	extern const std::string bold_magenta;
	extern const std::string bold_cyan;
	extern const std::string red;
	extern const std::string green;
	extern const std::string blue;
	extern const std::string magenta;
	extern const std::string yellow;
	extern const std::string cyan;
	extern const std::string gray;
	extern const std::string background_gray;
	extern std::string default_color;
}

class Message;

namespace debug
{
	void	check_leaks_atexit(std::string progname);
	void	logl(const std::string &msg, const std::string &color);	/* msg 뒤에 개행을 붙여 flush한다. */
	void	log_recv_status(const int sockfd, const ssize_t bytes, const std::string &packet);
	void	log_send_status(const int sockfd, const ssize_t bytes, const std::string &packet);
	void	log_msg_status(const Message &msg);
}
