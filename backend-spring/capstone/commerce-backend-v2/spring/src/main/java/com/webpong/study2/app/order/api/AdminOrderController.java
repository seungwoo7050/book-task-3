package com.webpong.study2.app.order.api;

import com.webpong.study2.app.global.api.PageResponse;
import com.webpong.study2.app.order.application.OrderService;
import com.webpong.study2.app.order.domain.OrderStatus;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin/orders")
public class AdminOrderController {

  private final OrderService orderService;

  public AdminOrderController(OrderService orderService) {
    this.orderService = orderService;
  }

  @GetMapping
  public PageResponse<OrderService.OrderSummary> listOrders(
      @RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "20") int size) {
    return orderService.listOrders("admin", page, size, true);
  }

  @PatchMapping("/{orderId}/status")
  public OrderService.OrderDetails updateStatus(
      @PathVariable long orderId, @Valid @RequestBody UpdateOrderStatusRequest request) {
    return orderService.updateStatus(orderId, request.status());
  }

  public record UpdateOrderStatusRequest(@NotNull OrderStatus status) {}
}
