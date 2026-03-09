package com.webpong.study2.app.global.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app.auth")
public record AuthProperties(
    String jwtSecret,
    long accessTokenSeconds,
    long refreshTokenSeconds,
    long oauthStateTtlSeconds,
    String googleClientId,
    String googleRedirectUri) {}
