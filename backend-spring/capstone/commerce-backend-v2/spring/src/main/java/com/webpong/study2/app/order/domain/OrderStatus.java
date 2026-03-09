package com.webpong.study2.app.order.domain;

public enum OrderStatus {
  PENDING_PAYMENT,
  PAID,
  CANCELLED,
  FULFILLED;

  public boolean canTransitionTo(OrderStatus nextStatus) {
    return switch (this) {
      case PENDING_PAYMENT -> nextStatus == PAID || nextStatus == CANCELLED;
      case PAID -> nextStatus == FULFILLED;
      case CANCELLED, FULFILLED -> false;
    };
  }
}
