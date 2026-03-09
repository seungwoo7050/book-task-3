package com.webpong.study2.app.auth.infrastructure;

import com.webpong.study2.app.global.config.FeatureProperties;
import java.time.Duration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

@Component("redisAttemptLimiter")
@ConditionalOnProperty(
    prefix = "app.features",
    name = "redis-rate-limit-enabled",
    havingValue = "true")
public class RedisAttemptLimiter implements AttemptLimiter {

  private final StringRedisTemplate stringRedisTemplate;

  public RedisAttemptLimiter(
      StringRedisTemplate stringRedisTemplate, FeatureProperties featureProperties) {
    this.stringRedisTemplate = stringRedisTemplate;
  }

  @Override
  public boolean allow(String bucket, int limit, long windowSeconds) {
    Long count = stringRedisTemplate.opsForValue().increment(bucket);
    if (count != null && count == 1L) {
      stringRedisTemplate.expire(bucket, Duration.ofSeconds(windowSeconds));
    }
    return count != null && count <= limit;
  }
}
