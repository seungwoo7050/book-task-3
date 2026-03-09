package com.webpong.study2.app.events.domain;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OutboxEventRepository extends JpaRepository<OutboxEventEntity, Long> {
  List<OutboxEventEntity> findByStatus(String status);
}
