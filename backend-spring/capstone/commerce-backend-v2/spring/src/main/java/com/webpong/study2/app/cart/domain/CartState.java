package com.webpong.study2.app.cart.domain;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.LinkedHashMap;
import java.util.Map;

public class CartState {

  private Map<Long, Integer> items = new LinkedHashMap<>();

  public CartState() {}

  public Map<Long, Integer> getItems() {
    return items;
  }

  public void setItems(Map<Long, Integer> items) {
    this.items = new LinkedHashMap<>(items);
  }

  public void add(long productId, int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be positive");
    }
    items.merge(productId, quantity, Integer::sum);
  }

  public void remove(long productId) {
    items.remove(productId);
  }

  @JsonIgnore
  public boolean isEmpty() {
    return items.isEmpty();
  }

  public CartState copy() {
    CartState state = new CartState();
    state.setItems(items);
    return state;
  }
}
