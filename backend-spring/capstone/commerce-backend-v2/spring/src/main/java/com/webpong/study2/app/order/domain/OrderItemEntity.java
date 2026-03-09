package com.webpong.study2.app.order.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "order_items")
public class OrderItemEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private Long orderId;

  @Column(nullable = false)
  private Long productId;

  @Column(nullable = false)
  private String productNameSnapshot;

  @Column(nullable = false, precision = 12, scale = 2)
  private BigDecimal unitPrice;

  @Column(nullable = false)
  private int quantity;

  @Column(nullable = false, precision = 12, scale = 2)
  private BigDecimal lineTotal;

  @Column(nullable = false)
  private Instant createdAt;

  protected OrderItemEntity() {}

  public OrderItemEntity(
      Long orderId,
      Long productId,
      String productNameSnapshot,
      BigDecimal unitPrice,
      int quantity,
      BigDecimal lineTotal) {
    this.orderId = orderId;
    this.productId = productId;
    this.productNameSnapshot = productNameSnapshot;
    this.unitPrice = unitPrice;
    this.quantity = quantity;
    this.lineTotal = lineTotal;
    this.createdAt = Instant.now();
  }

  public Long getOrderId() {
    return orderId;
  }

  public Long getProductId() {
    return productId;
  }

  public String getProductNameSnapshot() {
    return productNameSnapshot;
  }

  public BigDecimal getUnitPrice() {
    return unitPrice;
  }

  public int getQuantity() {
    return quantity;
  }

  public BigDecimal getLineTotal() {
    return lineTotal;
  }
}
