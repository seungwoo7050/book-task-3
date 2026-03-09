package com.webpong.study2.app;

import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.webpong.study2.app.order.domain.OrderEntity;
import com.webpong.study2.app.order.domain.OrderStatus;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class OrderStatusDomainTest {

  @Test
  void orderStatusTransitionsAreValidated() {
    OrderEntity order = new OrderEntity("user-1", BigDecimal.valueOf(19.99));
    order.transitionTo(OrderStatus.PAID);
    order.transitionTo(OrderStatus.FULFILLED);

    assertThatThrownBy(() -> order.transitionTo(OrderStatus.CANCELLED))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("Cannot transition");
  }
}
