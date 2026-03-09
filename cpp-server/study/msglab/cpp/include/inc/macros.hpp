#pragma once

#include "Executor.hpp"

#define BUILD_RPL_WELCOME(serv, network, nick, user, host)				":" + serv + " 001 " + nick + " :Welcome to the " + network + " Network " + nick + "!" + user + "@" + host + "\r\n"
#define BUILD_RPL_YOURHOST(serv, nick, version)							":" + serv + " 002 " + nick + " :Your host is " + serv + ", running version " + version + "\r\n"
#define BUILD_RPL_CREATED(serv, nick)									":" + serv + " 003 " + nick + " :This server was created sometime" + "\r\n"
#define BUILD_RPL_MYINFO(serv, nick, version, user_modes, chan_modes)	":" + serv + " 004 " + nick + " " + serv + " " + version + " " + user_modes + " " + chan_modes + "\r\n"

#define BUILD_RPL_AWAY(serv, nick, away_nick, away_msg)	                ":" + serv + " 301 " + nick + " " + away_nick + " :" + away_msg + "\r\n"
#define BUILD_RPL_CHANNELMODEIS(serv, channel, mode)	            ":" + serv + " 324 " + channel + " " + mode + "\r\n"
#define BUILD_RPL_NOTOPIC(serv, nick, channel)	                        ":" + serv + " 331 " + nick + " " + channel + " :No topic is set\r\n"
#define BUILD_RPL_TOPIC(serv, nick, channel, topic)	                    ":" + serv + " 332 " + nick + " " + channel + " :" + topic + "\r\n"
#define BUILD_RPL_TOPICWHOTIME(serv, nick, channel, topic_setter, topic_time) ":" + serv + " 333 " + nick + " " + channel + " " + topic_setter + " " + topic_time + "\r\n"

#define BUILD_RPL_INVITING(serv, nick, target, channel)	":" + serv + " 341 " + nick + " " + target + " " + channel + "\r\n"

#define BUILD_RPL_ENDOFNAMES(serv, nick, chan) ":" + serv + " 366 " + nick + " " + chan + " ::End of /NAMES list \r\n"

#define BUILD_ERR_NOSUCHNICK(serv, nick, target)		":" + serv + " 401 " + nick + " " + target + " :No such nick/channel\r\n"
#define BUILD_ERR_NOSUCHCHANNEL(serv, nick, chan)       ":" + serv + " 403 " + nick + " " + chan + " :No such channel\r\n"
#define BUILD_ERR_CANNOTSENDTOCHAN(serv, nick, channel)	":" + serv + " 404 " + nick + " " + channel + " :Cannot send to channel\r\n"
#define BUILD_ERR_TOOMANYCHANNELS(serv, nick, chan)     ":" + serv + " 405 " + nick + " " + chan + " :You have joined too many channels\r\n"
#define BUILD_ERR_TOOMANYTARGETS(serv, nick, target)	":" + serv + " 407 " + nick + " " + target + " :Too many targets\r\n"
#define BUILD_ERR_NORECIPIENT(serv, nick, command)		":" + serv + " 411 " + nick + " :No recipient given (" + command + ")\r\n"
#define BUILD_ERR_NOTEXTTOSEND(serv, nick)				":" + serv + " 412 " + nick + " :No text to send\r\n"
#define BUILD_ERR_NOTOPLEVEL(serv, nick, mask)			":" + serv + " 413 " + nick + " " + mask + " :No toplevel domain specified\r\n"
#define BUILD_ERR_WILDTOPLEVEL(serv, nick, mask)		":" + serv + " 414 " + nick + " " + mask + " :Wildcard in toplevel domain\r\n"

#define BUILD_ERR_UNKNOWNCOMMAND(serv, nick, command)	":" + serv + " 421 " + nick + " " + command + " :Unknown command\r\n"

#define BUILD_ERR_NONICKNAMEGIVEN(serv)			":" + serv + " 431 :No nickname given\r\n"
#define BUILD_ERR_ERRONEUSNICKNAME(serv, nick)	":" + serv + " 432 " + nick + " :Erroneous nickname\r\n"
#define BUILD_ERR_NICKNAMEINUSE(serv, nick)		":" + serv + " 433 " + nick + " :Nickname is already in use\r\n"

#define BUILD_ERR_USERNOTINCHANNEL(serv, nick, channel)	":" + serv + " 441 " + nick + " " + channel + " :They aren't on that channel\r\n"
#define BUILD_ERR_NOTONCHANNEL(serv, nick, channel)	":" + serv + " 442 " + nick + " " + channel + " :You're not on that channel\r\n"
#define BUILD_ERR_USERONCHANNEL(serv, nick, channel)	":" + serv + " 443 " + nick + " " + channel + " :is already on channel\r\n"
#define BUILD_ERR_NOTREGISTERED(serv, nick)		":" + serv + " 451 " + nick + " :You have not registered\r\n"

#define BUILD_ERR_NEEDMOREPARAMS(serv, comm)    ":" + serv + " 461 " + comm + " :Not enough parameters\r\n"
#define BUILD_ERR_ALREADYREGISTRED(serv, nick)  ":" + serv + " 462 " + nick + " :Unauthorized command (already registered)\r\n"
#define BUILD_ERR_PASSWDMISMATCH(serv)          ":" + serv + " 464 :Password incorrect\r\n"

#define BUILD_ERR_CHANNELISFULL(serv, nick, chan) ":" + serv + " 471 " + nick + " " + chan + " :Cannot join channel (+l)\r\n"
#define BUILD_ERR_UNKNOWNMODE(serv, nick, mode)	":" + serv + " 472 " + nick + " " + mode + " :is unknown mode char to me\r\n"
#define BUILD_ERR_INVITEONLYCHAN(serv, nick, chan) ":" + serv + " 473 " + nick + " " + chan + " :Cannot join channel (+i)\r\n"
#define BUILD_ERR_BADCHANNELKEY(serv, nick, chan) ":" + serv + " 475 " + nick + " " + chan + " :Cannot join channel (+k)\r\n"
#define BUILD_ERR_CHANOPRIVSNEEDED(serv, channel)	":" + serv + " 482 " + channel + " :You're not channel operator\r\n"
