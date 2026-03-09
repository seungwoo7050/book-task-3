#pragma once

#include "Executor.hpp"

class Executor
{
    static void     _execute_join(Server &server, Connection *&node, const Message &msg);
};
