SHELL := /bin/sh
NAME := eventlabd

CXX := c++
CXXFLAGS := -Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread
CPPFLAGS := -I include -I include/inc

SRCS := \
	src/EventManager.cpp \
	src/Server.cpp \
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
	python3 tests/test_eventlab.py

-include $(DEPS)
