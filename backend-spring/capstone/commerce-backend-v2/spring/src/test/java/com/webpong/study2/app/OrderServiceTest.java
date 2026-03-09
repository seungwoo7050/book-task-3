package com.webpong.study2.app;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import com.webpong.study2.app.cart.application.CartService;
import com.webpong.study2.app.cart.domain.CartState;
import com.webpong.study2.app.catalog.domain.ProductEntity;
import com.webpong.study2.app.catalog.domain.ProductRepository;
import com.webpong.study2.app.global.error.ConflictException;
import com.webpong.study2.app.order.application.OrderService;
import com.webpong.study2.app.order.domain.InventoryReservationRepository;
import com.webpong.study2.app.order.domain.OrderItemRepository;
import com.webpong.study2.app.order.domain.OrderRepository;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

  @Mock private OrderRepository orderRepository;
  @Mock private OrderItemRepository orderItemRepository;
  @Mock private InventoryReservationRepository inventoryReservationRepository;
  @Mock private ProductRepository productRepository;
  @Mock private CartService cartService;

  private OrderService orderService;

  @BeforeEach
  void setUp() {
    orderService =
        new OrderService(
            orderRepository,
            orderItemRepository,
            inventoryReservationRepository,
            productRepository,
            cartService);
  }

  @Test
  void checkoutTurnsOptimisticLockingFailureIntoConflict() {
    CartState cartState = new CartState();
    cartState.add(1L, 1);
    ProductEntity product =
        new ProductEntity(10L, "Keyboard", "Mechanical keyboard", BigDecimal.valueOf(49.99), 1);
    ReflectionTestUtils.setField(product, "id", 1L);

    when(cartService.requireCartState("user-1")).thenReturn(cartState);
    when(productRepository.findAllById(any(Iterable.class))).thenReturn(List.of(product));
    doThrow(new OptimisticLockingFailureException("stale version")).when(productRepository).flush();

    assertThatThrownBy(() -> orderService.checkout("user-1"))
        .isInstanceOf(ConflictException.class)
        .hasMessageContaining("Inventory changed");
  }
}
