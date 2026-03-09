package com.webpong.study2.app.auth.infrastructure;

import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnMissingBean(name = "redisAttemptLimiter")
public class InMemoryAttemptLimiter implements AttemptLimiter {

  private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

  @Override
  public synchronized boolean allow(String bucket, int limit, long windowSeconds) {
    Bucket current = buckets.get(bucket);
    Instant now = Instant.now();
    if (current == null || current.resetAt().isBefore(now)) {
      buckets.put(bucket, new Bucket(1, now.plusSeconds(windowSeconds)));
      return true;
    }
    if (current.count() >= limit) {
      return false;
    }
    buckets.put(bucket, new Bucket(current.count() + 1, current.resetAt()));
    return true;
  }

  private record Bucket(int count, Instant resetAt) {}
}
