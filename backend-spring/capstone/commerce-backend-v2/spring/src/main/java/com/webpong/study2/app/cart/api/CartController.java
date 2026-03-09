package com.webpong.study2.app.cart.api;

import com.webpong.study2.app.cart.application.CartService;
import com.webpong.study2.app.global.security.AuthenticationFacade;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/cart")
public class CartController {

  private final CartService cartService;
  private final AuthenticationFacade authenticationFacade;

  public CartController(CartService cartService, AuthenticationFacade authenticationFacade) {
    this.cartService = cartService;
    this.authenticationFacade = authenticationFacade;
  }

  @GetMapping("/items")
  public CartService.CartResponse getCart() {
    return cartService.getCart(authenticationFacade.currentUser().userId());
  }

  @PostMapping("/items")
  public CartService.CartResponse addItem(@Valid @RequestBody AddCartItemRequest request) {
    return cartService.addItem(
        authenticationFacade.currentUser().userId(), request.productId(), request.quantity());
  }

  @DeleteMapping("/items/{productId}")
  public CartService.CartResponse removeItem(@PathVariable long productId) {
    return cartService.removeItem(authenticationFacade.currentUser().userId(), productId);
  }

  public record AddCartItemRequest(@NotNull Long productId, @Min(1) int quantity) {}
}
