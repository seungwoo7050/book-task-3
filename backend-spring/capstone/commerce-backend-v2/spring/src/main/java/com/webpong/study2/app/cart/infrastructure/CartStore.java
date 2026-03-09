package com.webpong.study2.app.cart.infrastructure;

import com.webpong.study2.app.cart.domain.CartState;

public interface CartStore {

  CartState load(String userId);

  void save(String userId, CartState cartState);

  void clear(String userId);
}
