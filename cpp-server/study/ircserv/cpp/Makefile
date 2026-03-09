SHELL := /bin/sh
NAME := ircserv

CXX := c++
CXXFLAGS := -Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread
CPPFLAGS := -I include -I include/inc

SRCS := \
	src/Channel.cpp \
	src/Connection.cpp \
	src/EventManager.cpp \
	src/Executor.cpp \
	src/Message.cpp \
	src/Parser.cpp \
	src/Server.cpp \
	src/debug.cpp \
	src/execute_join.cpp \
	src/main.cpp \
	src/utils.cpp

OBJS := $(SRCS:.cpp=.o)
DEPS := $(OBJS:.o=.d)

.PHONY: all clean fclean re test

all: $(NAME)

$(NAME): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJS) $(DEPS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

test: $(NAME)
	python3 tests/test_irc_join.py

-include $(DEPS)
