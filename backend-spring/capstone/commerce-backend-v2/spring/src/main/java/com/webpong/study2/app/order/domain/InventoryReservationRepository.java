package com.webpong.study2.app.order.domain;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InventoryReservationRepository
    extends JpaRepository<InventoryReservationEntity, Long> {

  List<InventoryReservationEntity> findByOrderId(Long orderId);
}
