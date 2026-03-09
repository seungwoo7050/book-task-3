package com.webpong.study2.app.commerce.application;

import com.webpong.study2.app.commerce.domain.CartItemEntity;
import com.webpong.study2.app.commerce.domain.CartItemRepository;
import com.webpong.study2.app.commerce.domain.CommerceProductEntity;
import com.webpong.study2.app.commerce.domain.CommerceProductRepository;
import com.webpong.study2.app.commerce.domain.OrderEntity;
import com.webpong.study2.app.commerce.domain.OrderRepository;
import java.math.BigDecimal;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CommerceService {

  private final CommerceProductRepository productRepository;
  private final CartItemRepository cartItemRepository;
  private final OrderRepository orderRepository;

  public CommerceService(
      CommerceProductRepository productRepository,
      CartItemRepository cartItemRepository,
      OrderRepository orderRepository) {
    this.productRepository = productRepository;
    this.cartItemRepository = cartItemRepository;
    this.orderRepository = orderRepository;
  }

  @Transactional
  public ProductResponse createProduct(String name, BigDecimal price, int stock) {
    return ProductResponse.from(
        productRepository.save(new CommerceProductEntity(name, price, stock)));
  }

  @Transactional(readOnly = true)
  public List<ProductResponse> listProducts() {
    return productRepository.findAll().stream().map(ProductResponse::from).toList();
  }

  @Transactional
  public CartResponse addCartItem(String customerEmail, long productId, int quantity) {
    cartItemRepository.save(new CartItemEntity(customerEmail, productId, quantity));
    return new CartResponse(
        customerEmail, cartItemRepository.findByCustomerEmail(customerEmail).size());
  }

  @Transactional
  public OrderResponse checkout(String customerEmail) {
    List<CartItemEntity> items = cartItemRepository.findByCustomerEmail(customerEmail);
    if (items.isEmpty()) {
      throw new IllegalArgumentException("Cart is empty");
    }
    int totalQuantity = 0;
    for (CartItemEntity item : items) {
      CommerceProductEntity product =
          productRepository
              .findById(item.getProductId())
              .orElseThrow(() -> new IllegalArgumentException("Product not found"));
      if (product.getStock() < item.getQuantity()) {
        throw new IllegalArgumentException("Not enough stock");
      }
      product.decrementStock(item.getQuantity());
      totalQuantity += item.getQuantity();
    }
    OrderEntity order =
        orderRepository.save(new OrderEntity(customerEmail, totalQuantity, "PLACED"));
    cartItemRepository.deleteByCustomerEmail(customerEmail);
    return new OrderResponse(
        order.getId(), order.getCustomerEmail(), order.getStatus(), order.getTotalQuantity());
  }

  @Transactional(readOnly = true)
  public List<OrderResponse> listOrders() {
    return orderRepository.findAll().stream()
        .map(
            order ->
                new OrderResponse(
                    order.getId(),
                    order.getCustomerEmail(),
                    order.getStatus(),
                    order.getTotalQuantity()))
        .toList();
  }

  public record ProductResponse(Long id, String name, BigDecimal price, int stock) {
    public static ProductResponse from(CommerceProductEntity entity) {
      return new ProductResponse(
          entity.getId(), entity.getName(), entity.getPrice(), entity.getStock());
    }
  }

  public record CartResponse(String customerEmail, int itemCount) {}

  public record OrderResponse(Long id, String customerEmail, String status, int totalQuantity) {}
}
