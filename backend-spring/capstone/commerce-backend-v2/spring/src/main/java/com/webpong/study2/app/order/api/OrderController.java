package com.webpong.study2.app.order.api;

import com.webpong.study2.app.global.api.PageResponse;
import com.webpong.study2.app.global.security.AuthenticationFacade;
import com.webpong.study2.app.order.application.OrderService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

  private final OrderService orderService;
  private final AuthenticationFacade authenticationFacade;

  public OrderController(OrderService orderService, AuthenticationFacade authenticationFacade) {
    this.orderService = orderService;
    this.authenticationFacade = authenticationFacade;
  }

  @PostMapping
  public OrderService.OrderDetails checkout() {
    return orderService.checkout(authenticationFacade.currentUser().userId());
  }

  @GetMapping
  public PageResponse<OrderService.OrderSummary> listOrders(
      @RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "20") int size) {
    return orderService.listOrders(authenticationFacade.currentUser().userId(), page, size, false);
  }

  @GetMapping("/{orderId}")
  public OrderService.OrderDetails getOrder(@PathVariable long orderId) {
    return orderService.getOrderForUser(
        authenticationFacade.currentUser().userId(), orderId, false);
  }
}
