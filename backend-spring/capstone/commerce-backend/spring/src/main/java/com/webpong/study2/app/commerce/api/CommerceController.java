package com.webpong.study2.app.commerce.api;

import com.webpong.study2.app.commerce.application.CommerceService;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.math.BigDecimal;
import java.util.List;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1")
public class CommerceController {

  private final CommerceService commerceService;

  public CommerceController(CommerceService commerceService) {
    this.commerceService = commerceService;
  }

  @GetMapping("/products")
  public List<CommerceService.ProductResponse> products() {
    return commerceService.listProducts();
  }

  @PostMapping("/admin/products")
  public CommerceService.ProductResponse createProduct(@RequestBody CreateProductRequest request) {
    return commerceService.createProduct(request.name(), request.price(), request.stock());
  }

  @PostMapping("/cart/items")
  public CommerceService.CartResponse addCartItem(@RequestBody AddCartItemRequest request) {
    return commerceService.addCartItem(
        request.customerEmail(), request.productId(), request.quantity());
  }

  @PostMapping("/orders")
  public CommerceService.OrderResponse checkout(@RequestParam @Email String customerEmail) {
    return commerceService.checkout(customerEmail);
  }

  @GetMapping("/admin/orders")
  public List<CommerceService.OrderResponse> orders() {
    return commerceService.listOrders();
  }

  public record CreateProductRequest(
      @NotBlank String name, @Min(0) BigDecimal price, @Min(1) int stock) {}

  public record AddCartItemRequest(
      @Email String customerEmail, long productId, @Min(1) int quantity) {}
}
