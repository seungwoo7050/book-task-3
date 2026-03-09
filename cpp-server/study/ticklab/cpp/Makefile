SHELL := /bin/sh
NAME := ticklab_tests

CXX := c++
CXXFLAGS := -Wall -Wextra -Werror -std=c++17 -MMD -MP
CPPFLAGS := -I include -I include/inc

SRCS := \
	src/MatchEngine.cpp \
	tests/test_ticklab.cpp

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
	./$(NAME)

-include $(DEPS)
