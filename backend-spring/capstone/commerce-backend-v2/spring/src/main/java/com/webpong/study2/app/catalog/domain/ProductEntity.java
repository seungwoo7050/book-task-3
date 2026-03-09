package com.webpong.study2.app.catalog.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "products")
public class ProductEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private Long categoryId;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, length = 1000)
  private String description;

  @Column(nullable = false, precision = 12, scale = 2)
  private BigDecimal price;

  @Column(nullable = false)
  private int stock;

  @Column(nullable = false)
  private boolean active;

  @Version
  @Column(nullable = false)
  private Long version;

  @Column(nullable = false)
  private Instant createdAt;

  @Column(nullable = false)
  private Instant updatedAt;

  protected ProductEntity() {}

  public ProductEntity(
      Long categoryId, String name, String description, BigDecimal price, int stock) {
    this.categoryId = categoryId;
    this.name = name;
    this.description = description;
    this.price = price;
    this.stock = stock;
    this.active = true;
    this.createdAt = Instant.now();
    this.updatedAt = this.createdAt;
  }

  public Long getId() {
    return id;
  }

  public Long getCategoryId() {
    return categoryId;
  }

  public String getName() {
    return name;
  }

  public String getDescription() {
    return description;
  }

  public BigDecimal getPrice() {
    return price;
  }

  public int getStock() {
    return stock;
  }

  public boolean isActive() {
    return active;
  }

  public Long getVersion() {
    return version;
  }

  public Instant getCreatedAt() {
    return createdAt;
  }

  public Instant getUpdatedAt() {
    return updatedAt;
  }

  public void update(
      Long categoryId,
      String name,
      String description,
      BigDecimal price,
      int stock,
      boolean active) {
    this.categoryId = categoryId;
    this.name = name;
    this.description = description;
    this.price = price;
    this.stock = stock;
    this.active = active;
    this.updatedAt = Instant.now();
  }

  public void deactivate() {
    this.active = false;
    this.updatedAt = Instant.now();
  }

  public void reserve(int quantity) {
    if (!active) {
      throw new IllegalArgumentException("Inactive products cannot be ordered");
    }
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be positive");
    }
    if (stock < quantity) {
      throw new IllegalArgumentException("Insufficient stock for product " + id);
    }
    this.stock -= quantity;
    this.updatedAt = Instant.now();
  }

  public void release(int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be positive");
    }
    this.stock += quantity;
    this.updatedAt = Instant.now();
  }
}
