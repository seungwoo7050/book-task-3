package com.webpong.study2.app.cache.application;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class CacheConcurrencyDemoService {

  private final Map<String, Integer> inventory = new ConcurrentHashMap<>();
  private final Map<String, ReservationResult> idempotency = new ConcurrentHashMap<>();

  public CacheConcurrencyDemoService() {
    inventory.put("SKU-1", 10);
    inventory.put("SKU-2", 5);
  }

  public synchronized ReservationResult reserve(String sku, int quantity, String idempotencyKey) {
    if (idempotency.containsKey(idempotencyKey)) {
      return idempotency.get(idempotencyKey);
    }

    int available = inventory.getOrDefault(sku, 0);
    if (available < quantity) {
      throw new IllegalArgumentException("Not enough inventory");
    }

    inventory.put(sku, available - quantity);
    ReservationResult result =
        new ReservationResult(sku, quantity, inventory.get(sku), idempotencyKey);
    idempotency.put(idempotencyKey, result);
    return result;
  }

  @Cacheable("inventory-status")
  public InventoryStatus inventoryStatus(String sku) {
    return new InventoryStatus(sku, inventory.getOrDefault(sku, 0));
  }

  public record ReservationResult(String sku, int quantity, int remaining, String idempotencyKey) {}

  public record InventoryStatus(String sku, int available) {}
}
