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

    static unsigned lbit;   /* client 수 제한 */
    static unsigned ibit;   /* invite 전용 */
    static unsigned tbit;   /* operator만 topic 변경 */
    static unsigned kbit;   /* key 필요 */
    
    unsigned                                state;
    std::map<int, Connection *>             clientdb;
    std::map<Connection *, enum CHANOPS>    privdb;
    std::map<int, Connection *>             invitedb;

    std::string name; // 최대 200자다. '&' 또는 '#'로 시작하고, 공백·ASCII 7·comma는 허용하지 않는다.
    unsigned    limit;  // lbit가 켜졌을 때 적용할 client 수 제한
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
