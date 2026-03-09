package com.webpong.study2.app.cart.infrastructure;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.cart.domain.CartState;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component("redisCartStore")
@ConditionalOnProperty(prefix = "app.features", name = "redis-cart-enabled", havingValue = "true")
public class RedisCartStore implements CartStore {

  private final StringRedisTemplate stringRedisTemplate;
  private final ObjectMapper objectMapper;

  public RedisCartStore(StringRedisTemplate stringRedisTemplate, ObjectMapper objectMapper) {
    this.stringRedisTemplate = stringRedisTemplate;
    this.objectMapper = objectMapper;
  }

  @Override
  public CartState load(String userId) {
    String raw = stringRedisTemplate.opsForValue().get(key(userId));
    if (!StringUtils.hasText(raw)) {
      return new CartState();
    }
    try {
      return objectMapper.readValue(raw, CartState.class);
    } catch (JsonProcessingException exception) {
      throw new IllegalStateException("Cart payload could not be parsed", exception);
    }
  }

  @Override
  public void save(String userId, CartState cartState) {
    try {
      stringRedisTemplate
          .opsForValue()
          .set(key(userId), objectMapper.writeValueAsString(cartState));
    } catch (JsonProcessingException exception) {
      throw new IllegalStateException("Cart payload could not be serialized", exception);
    }
  }

  @Override
  public void clear(String userId) {
    stringRedisTemplate.delete(key(userId));
  }

  private String key(String userId) {
    return "cart:" + userId;
  }
}
