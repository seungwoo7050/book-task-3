package com.webpong.study2.app.auth.infrastructure;

public interface AttemptLimiter {
  boolean allow(String bucket, int limit, long windowSeconds);
}
