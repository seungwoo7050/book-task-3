package com.webpong.study2.app.payment.domain;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PaymentRepository extends JpaRepository<PaymentEntity, Long> {

  Optional<PaymentEntity> findByIdempotencyKey(String idempotencyKey);

  Optional<PaymentEntity> findByOrderId(Long orderId);
}
