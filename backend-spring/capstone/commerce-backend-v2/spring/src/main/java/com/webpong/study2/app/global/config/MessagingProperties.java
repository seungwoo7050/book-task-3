package com.webpong.study2.app.global.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app.messaging")
public record MessagingProperties(String orderPaidTopic, long publishDelayMs) {}
