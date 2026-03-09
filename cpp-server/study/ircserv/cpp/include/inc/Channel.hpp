#pragma once

#include <string>

#include <map>

class Connection;

class Channel
{
    public:
    static enum CHANOPS
    {
        OPERATOR
    } chanops;

    static unsigned lbit;   /* client limit */
    static unsigned ibit;   /* invite only */
    static unsigned tbit;   /* protected topic */
    static unsigned kbit;   /* key required */
    
    unsigned                                state;
    std::map<int, Connection *>             clientdb;
    std::map<Connection *, enum CHANOPS>    privdb;
    std::map<int, Connection *>             invitedb;

    std::string name; // max 200 (50?), beginning with '&' or '#' (or '+' or '!'?); no spaces; no ASCII 7; no comma
    unsigned    limit;  // client limit when lbit is set
    std::string topic;
    std::string topic_time;
    std::string topic_setter;

    std::string key;


    public:
    unsigned    rdstate() const;
    void        join(Connection *&client);
    virtual void        part(Connection *&client);

    public:
    Channel(const std::string &channelname, Connection *founder);
    virtual ~Channel();

    std::string get_mode_string() const {
        std::string ret;
        if (this->state & lbit) ret += "l";
        if (this->state & ibit) ret += "i";
        if (this->state & tbit) ret += "t";
        if (this->state & kbit) ret += "k";
        return ret.empty() ? "+" : "+" + ret;
    }
};
