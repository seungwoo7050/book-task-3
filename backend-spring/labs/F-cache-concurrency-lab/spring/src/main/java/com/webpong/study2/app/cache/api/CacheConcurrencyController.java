package com.webpong.study2.app.cache.api;

import com.webpong.study2.app.cache.application.CacheConcurrencyDemoService;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1/inventory")
public class CacheConcurrencyController {

  private final CacheConcurrencyDemoService service;

  public CacheConcurrencyController(CacheConcurrencyDemoService service) {
    this.service = service;
  }

  @PostMapping("/reservations")
  public CacheConcurrencyDemoService.ReservationResult reserve(
      @RequestHeader("Idempotency-Key") String idempotencyKey,
      @RequestBody ReservationRequest request) {
    return service.reserve(request.sku(), request.quantity(), idempotencyKey);
  }

  @GetMapping("/{sku}")
  public CacheConcurrencyDemoService.InventoryStatus inventory(@PathVariable String sku) {
    return service.inventoryStatus(sku);
  }

  public record ReservationRequest(@NotBlank String sku, @Min(1) int quantity) {}
}
