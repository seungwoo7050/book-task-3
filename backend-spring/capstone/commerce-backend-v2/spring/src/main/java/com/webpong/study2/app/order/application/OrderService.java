package com.webpong.study2.app.order.application;

import com.webpong.study2.app.cart.application.CartService;
import com.webpong.study2.app.cart.domain.CartState;
import com.webpong.study2.app.catalog.domain.ProductEntity;
import com.webpong.study2.app.catalog.domain.ProductRepository;
import com.webpong.study2.app.global.api.PageResponse;
import com.webpong.study2.app.global.error.ConflictException;
import com.webpong.study2.app.global.error.ForbiddenException;
import com.webpong.study2.app.global.error.NotFoundException;
import com.webpong.study2.app.order.domain.InventoryReservationEntity;
import com.webpong.study2.app.order.domain.InventoryReservationRepository;
import com.webpong.study2.app.order.domain.OrderEntity;
import com.webpong.study2.app.order.domain.OrderItemEntity;
import com.webpong.study2.app.order.domain.OrderItemRepository;
import com.webpong.study2.app.order.domain.OrderRepository;
import com.webpong.study2.app.order.domain.OrderStatus;
import jakarta.persistence.OptimisticLockException;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {

  private final OrderRepository orderRepository;
  private final OrderItemRepository orderItemRepository;
  private final InventoryReservationRepository inventoryReservationRepository;
  private final ProductRepository productRepository;
  private final CartService cartService;

  public OrderService(
      OrderRepository orderRepository,
      OrderItemRepository orderItemRepository,
      InventoryReservationRepository inventoryReservationRepository,
      ProductRepository productRepository,
      CartService cartService) {
    this.orderRepository = orderRepository;
    this.orderItemRepository = orderItemRepository;
    this.inventoryReservationRepository = inventoryReservationRepository;
    this.productRepository = productRepository;
    this.cartService = cartService;
  }

  @Transactional
  public OrderDetails checkout(String userId) {
    CartState cartState = cartService.requireCartState(userId);
    Map<Long, ProductEntity> products =
        productRepository.findAllById(cartState.getItems().keySet()).stream()
            .collect(java.util.stream.Collectors.toMap(ProductEntity::getId, Function.identity()));
    if (products.size() != cartState.getItems().size()) {
      throw new NotFoundException("One or more products no longer exist");
    }

    BigDecimal totalAmount = BigDecimal.ZERO;
    try {
      for (Map.Entry<Long, Integer> entry : cartState.getItems().entrySet()) {
        ProductEntity product = products.get(entry.getKey());
        product.reserve(entry.getValue());
        totalAmount =
            totalAmount.add(product.getPrice().multiply(BigDecimal.valueOf(entry.getValue())));
      }
      productRepository.flush();
    } catch (IllegalArgumentException
        | OptimisticLockException
        | OptimisticLockingFailureException exception) {
      throw new ConflictException("Inventory changed during checkout. Retry the request.");
    }

    OrderEntity order = orderRepository.save(new OrderEntity(userId, totalAmount));
    for (Map.Entry<Long, Integer> entry : cartState.getItems().entrySet()) {
      ProductEntity product = products.get(entry.getKey());
      BigDecimal lineTotal = product.getPrice().multiply(BigDecimal.valueOf(entry.getValue()));
      orderItemRepository.save(
          new OrderItemEntity(
              order.getId(),
              product.getId(),
              product.getName(),
              product.getPrice(),
              entry.getValue(),
              lineTotal));
      inventoryReservationRepository.save(
          new InventoryReservationEntity(order.getId(), product.getId(), entry.getValue()));
    }
    cartService.clearCart(userId);
    return getOrderForUser(userId, order.getId(), false);
  }

  @Transactional(readOnly = true)
  public PageResponse<OrderSummary> listOrders(String userId, int page, int size, boolean admin) {
    Page<OrderEntity> orders =
        admin
            ? orderRepository.findAll(
                PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "id")))
            : orderRepository.findByUserId(
                userId, PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "id")));
    return PageResponse.from(orders.map(this::toSummary));
  }

  @Transactional(readOnly = true)
  public OrderDetails getOrderForUser(String userId, long orderId, boolean admin) {
    OrderEntity order = requireOrder(orderId);
    if (!admin && !order.getUserId().equals(userId)) {
      throw new ForbiddenException("Order access is forbidden");
    }
    return toDetails(order);
  }

  @Transactional
  public OrderDetails updateStatus(long orderId, OrderStatus nextStatus) {
    OrderEntity order = requireOrder(orderId);
    if (nextStatus == OrderStatus.CANCELLED) {
      releaseReservations(order);
    }
    order.transitionTo(nextStatus);
    return toDetails(order);
  }

  @Transactional(readOnly = true)
  public OrderEntity requireOrder(long orderId) {
    return orderRepository
        .findById(orderId)
        .orElseThrow(() -> new NotFoundException("Order not found"));
  }

  @Transactional
  public void confirmReservations(long orderId) {
    inventoryReservationRepository
        .findByOrderId(orderId)
        .forEach(InventoryReservationEntity::confirm);
  }

  @Transactional
  public void releaseReservations(OrderEntity order) {
    List<InventoryReservationEntity> reservations =
        inventoryReservationRepository.findByOrderId(order.getId()).stream()
            .filter(
                reservation ->
                    reservation.getStatus()
                        != com.webpong.study2.app.order.domain.ReservationStatus.RELEASED)
            .toList();
    if (reservations.isEmpty()) {
      return;
    }
    Map<Long, ProductEntity> products =
        productRepository
            .findAllById(
                reservations.stream().map(InventoryReservationEntity::getProductId).toList())
            .stream()
            .collect(java.util.stream.Collectors.toMap(ProductEntity::getId, Function.identity()));
    reservations.forEach(
        reservation -> {
          ProductEntity product = products.get(reservation.getProductId());
          product.release(reservation.getQuantity());
          reservation.release();
        });
  }

  private OrderSummary toSummary(OrderEntity order) {
    return new OrderSummary(
        order.getId(), order.getStatus(), order.getTotalAmount(), order.getCreatedAt());
  }

  private OrderDetails toDetails(OrderEntity order) {
    List<OrderLine> lines =
        orderItemRepository.findByOrderId(order.getId()).stream()
            .map(
                item ->
                    new OrderLine(
                        item.getProductId(),
                        item.getProductNameSnapshot(),
                        item.getUnitPrice(),
                        item.getQuantity(),
                        item.getLineTotal()))
            .toList();
    return new OrderDetails(
        order.getId(),
        order.getUserId(),
        order.getStatus(),
        order.getTotalAmount(),
        lines,
        order.getCreatedAt());
  }

  public record OrderSummary(
      Long orderId, OrderStatus status, BigDecimal totalAmount, java.time.Instant createdAt) {}

  public record OrderLine(
      Long productId,
      String productName,
      BigDecimal unitPrice,
      int quantity,
      BigDecimal lineTotal) {}

  public record OrderDetails(
      Long orderId,
      String userId,
      OrderStatus status,
      BigDecimal totalAmount,
      List<OrderLine> items,
      java.time.Instant createdAt) {}
}
