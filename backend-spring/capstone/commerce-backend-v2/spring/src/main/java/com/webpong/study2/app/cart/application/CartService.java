package com.webpong.study2.app.cart.application;

import com.webpong.study2.app.cart.domain.CartState;
import com.webpong.study2.app.cart.infrastructure.CartStore;
import com.webpong.study2.app.catalog.domain.ProductEntity;
import com.webpong.study2.app.catalog.domain.ProductRepository;
import com.webpong.study2.app.global.error.NotFoundException;
import java.math.BigDecimal;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CartService {

  private final CartStore cartStore;
  private final ProductRepository productRepository;

  public CartService(CartStore cartStore, ProductRepository productRepository) {
    this.cartStore = cartStore;
    this.productRepository = productRepository;
  }

  @Transactional(readOnly = true)
  public CartResponse getCart(String userId) {
    return toResponse(cartStore.load(userId));
  }

  @Transactional(readOnly = true)
  public CartState requireCartState(String userId) {
    CartState cartState = cartStore.load(userId);
    if (cartState.isEmpty()) {
      throw new IllegalArgumentException("Cart is empty");
    }
    return cartState;
  }

  @Transactional
  public CartResponse addItem(String userId, long productId, int quantity) {
    ProductEntity product =
        productRepository
            .findById(productId)
            .orElseThrow(() -> new NotFoundException("Product not found"));
    if (!product.isActive()) {
      throw new IllegalArgumentException("Inactive products cannot be added to cart");
    }
    CartState cartState = cartStore.load(userId);
    cartState.add(productId, quantity);
    cartStore.save(userId, cartState);
    return toResponse(cartState);
  }

  @Transactional
  public CartResponse removeItem(String userId, long productId) {
    CartState cartState = cartStore.load(userId);
    cartState.remove(productId);
    cartStore.save(userId, cartState);
    return toResponse(cartState);
  }

  @Transactional
  public void clearCart(String userId) {
    cartStore.clear(userId);
  }

  private CartResponse toResponse(CartState cartState) {
    if (cartState.getItems().isEmpty()) {
      return new CartResponse(List.of(), 0, BigDecimal.ZERO);
    }
    Map<Long, ProductEntity> products =
        productRepository.findAllById(cartState.getItems().keySet()).stream()
            .collect(java.util.stream.Collectors.toMap(ProductEntity::getId, Function.identity()));
    List<CartItemResponse> items =
        cartState.getItems().entrySet().stream()
            .sorted(Comparator.comparingLong(Map.Entry::getKey))
            .map(
                entry -> {
                  ProductEntity product = products.get(entry.getKey());
                  if (product == null) {
                    throw new NotFoundException("Product not found");
                  }
                  BigDecimal lineTotal =
                      product.getPrice().multiply(BigDecimal.valueOf(entry.getValue()));
                  return new CartItemResponse(
                      product.getId(),
                      product.getName(),
                      product.getPrice(),
                      entry.getValue(),
                      lineTotal);
                })
            .toList();
    BigDecimal totalAmount =
        items.stream().map(CartItemResponse::lineTotal).reduce(BigDecimal.ZERO, BigDecimal::add);
    int itemCount = items.stream().mapToInt(CartItemResponse::quantity).sum();
    return new CartResponse(items, itemCount, totalAmount);
  }

  public record CartResponse(List<CartItemResponse> items, int itemCount, BigDecimal totalAmount) {}

  public record CartItemResponse(
      Long productId,
      String productName,
      BigDecimal unitPrice,
      int quantity,
      BigDecimal lineTotal) {}
}
