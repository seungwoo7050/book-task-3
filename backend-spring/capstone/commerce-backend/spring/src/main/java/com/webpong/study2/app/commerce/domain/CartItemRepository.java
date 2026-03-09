package com.webpong.study2.app.commerce.domain;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CartItemRepository extends JpaRepository<CartItemEntity, Long> {
  List<CartItemEntity> findByCustomerEmail(String customerEmail);

  void deleteByCustomerEmail(String customerEmail);
}
