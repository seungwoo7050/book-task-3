package com.webpong.study2.app.payment.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "payments")
public class PaymentEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false, unique = true)
  private Long orderId;

  @Column(nullable = false, unique = true)
  private String idempotencyKey;

  @Column(nullable = false)
  private String provider;

  @Enumerated(EnumType.STRING)
  @Column(nullable = false)
  private PaymentStatus status;

  @Column(nullable = false, precision = 12, scale = 2)
  private BigDecimal amount;

  @Column(nullable = false)
  private Instant createdAt;

  @Column private Instant confirmedAt;

  protected PaymentEntity() {}

  public PaymentEntity(Long orderId, String idempotencyKey, BigDecimal amount) {
    this.orderId = orderId;
    this.idempotencyKey = idempotencyKey;
    this.provider = "mock";
    this.status = PaymentStatus.SUCCEEDED;
    this.amount = amount;
    this.createdAt = Instant.now();
    this.confirmedAt = this.createdAt;
  }

  public Long getId() {
    return id;
  }

  public Long getOrderId() {
    return orderId;
  }

  public String getIdempotencyKey() {
    return idempotencyKey;
  }

  public PaymentStatus getStatus() {
    return status;
  }

  public BigDecimal getAmount() {
    return amount;
  }

  public Instant getConfirmedAt() {
    return confirmedAt;
  }
}
