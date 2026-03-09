package com.webpong.study2.app;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.cart.domain.CartState;
import com.webpong.study2.app.cart.infrastructure.RedisCartStore;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

@ExtendWith(MockitoExtension.class)
class RedisCartStoreTest {

  @Mock private StringRedisTemplate stringRedisTemplate;
  @Mock private ValueOperations<String, String> valueOperations;

  @Test
  void cartPayloadCanBeSerializedAndReloaded() {
    AtomicReference<String> stored = new AtomicReference<>();
    when(stringRedisTemplate.opsForValue()).thenReturn(valueOperations);
    doAnswer(
            invocation -> {
              stored.set(invocation.getArgument(1, String.class));
              return null;
            })
        .when(valueOperations)
        .set(eq("cart:user-1"), anyString());
    when(valueOperations.get("cart:user-1")).thenAnswer(invocation -> stored.get());

    RedisCartStore redisCartStore = new RedisCartStore(stringRedisTemplate, new ObjectMapper());
    CartState cartState = new CartState();
    cartState.add(11L, 2);

    redisCartStore.save("user-1", cartState);
    CartState loaded = redisCartStore.load("user-1");

    assertThat(loaded.getItems()).containsEntry(11L, 2);
  }
}
