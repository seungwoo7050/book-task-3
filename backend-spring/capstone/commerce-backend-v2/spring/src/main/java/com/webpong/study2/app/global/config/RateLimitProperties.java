package com.webpong.study2.app.global.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app.rate-limit")
public record RateLimitProperties(
    int loginMaxAttempts,
    long loginWindowSeconds,
    int refreshMaxAttempts,
    long refreshWindowSeconds) {}
