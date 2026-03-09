package com.webpong.study2.app.global.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app.features")
public record FeatureProperties(
    boolean redisCartEnabled, boolean redisRateLimitEnabled, boolean messagingEnabled) {}
