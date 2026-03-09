package com.webpong.study2.app.cart.infrastructure;

import com.webpong.study2.app.cart.domain.CartState;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnMissingBean(name = "redisCartStore")
public class InMemoryCartStore implements CartStore {

  private final Map<String, CartState> carts = new ConcurrentHashMap<>();

  @Override
  public CartState load(String userId) {
    return carts.getOrDefault(userId, new CartState()).copy();
  }

  @Override
  public void save(String userId, CartState cartState) {
    carts.put(userId, cartState.copy());
  }

  @Override
  public void clear(String userId) {
    carts.remove(userId);
  }
}
