package com.webpong.study2.app.notification.domain;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NotificationRepository extends JpaRepository<NotificationEntity, Long> {

  Optional<NotificationEntity> findByDedupKey(String dedupKey);
}
