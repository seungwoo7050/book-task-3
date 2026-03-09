package com.webpong.study2.app.commerce.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "commerce_cart_items")
public class CartItemEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String customerEmail;
  private Long productId;
  private int quantity;

  protected CartItemEntity() {}

  public CartItemEntity(String customerEmail, Long productId, int quantity) {
    this.customerEmail = customerEmail;
    this.productId = productId;
    this.quantity = quantity;
  }

  public Long getId() {
    return id;
  }

  public String getCustomerEmail() {
    return customerEmail;
  }

  public Long getProductId() {
    return productId;
  }

  public int getQuantity() {
    return quantity;
  }
}
