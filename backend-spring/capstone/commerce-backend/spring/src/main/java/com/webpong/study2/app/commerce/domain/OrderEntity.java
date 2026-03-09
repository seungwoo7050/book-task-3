package com.webpong.study2.app.commerce.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "commerce_orders")
public class OrderEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String customerEmail;
  private int totalQuantity;
  private String status;

  protected OrderEntity() {}

  public OrderEntity(String customerEmail, int totalQuantity, String status) {
    this.customerEmail = customerEmail;
    this.totalQuantity = totalQuantity;
    this.status = status;
  }

  public Long getId() {
    return id;
  }

  public String getCustomerEmail() {
    return customerEmail;
  }

  public int getTotalQuantity() {
    return totalQuantity;
  }

  public String getStatus() {
    return status;
  }
}
