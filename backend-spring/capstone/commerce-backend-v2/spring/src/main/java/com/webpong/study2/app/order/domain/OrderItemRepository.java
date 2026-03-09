package com.webpong.study2.app.order.domain;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderItemRepository extends JpaRepository<OrderItemEntity, Long> {

  List<OrderItemEntity> findByOrderId(Long orderId);
}
