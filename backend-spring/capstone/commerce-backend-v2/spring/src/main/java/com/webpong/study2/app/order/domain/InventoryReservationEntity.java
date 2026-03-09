package com.webpong.study2.app.order.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "inventory_reservations")
public class InventoryReservationEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private Long orderId;

  @Column(nullable = false)
  private Long productId;

  @Column(nullable = false)
  private int quantity;

  @Enumerated(EnumType.STRING)
  @Column(nullable = false)
  private ReservationStatus status;

  @Column(nullable = false)
  private Instant createdAt;

  @Column(nullable = false)
  private Instant updatedAt;

  protected InventoryReservationEntity() {}

  public InventoryReservationEntity(Long orderId, Long productId, int quantity) {
    this.orderId = orderId;
    this.productId = productId;
    this.quantity = quantity;
    this.status = ReservationStatus.RESERVED;
    this.createdAt = Instant.now();
    this.updatedAt = this.createdAt;
  }

  public Long getOrderId() {
    return orderId;
  }

  public Long getProductId() {
    return productId;
  }

  public int getQuantity() {
    return quantity;
  }

  public ReservationStatus getStatus() {
    return status;
  }

  public void confirm() {
    this.status = ReservationStatus.CONFIRMED;
    this.updatedAt = Instant.now();
  }

  public void release() {
    this.status = ReservationStatus.RELEASED;
    this.updatedAt = Instant.now();
  }
}
