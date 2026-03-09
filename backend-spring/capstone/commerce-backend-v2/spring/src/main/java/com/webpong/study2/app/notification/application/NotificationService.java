package com.webpong.study2.app.notification.application;

import com.webpong.study2.app.auth.domain.AuditEventEntity;
import com.webpong.study2.app.auth.domain.AuditEventRepository;
import com.webpong.study2.app.notification.domain.NotificationEntity;
import com.webpong.study2.app.notification.domain.NotificationRepository;
import java.math.BigDecimal;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NotificationService {

  private final NotificationRepository notificationRepository;
  private final AuditEventRepository auditEventRepository;

  public NotificationService(
      NotificationRepository notificationRepository, AuditEventRepository auditEventRepository) {
    this.notificationRepository = notificationRepository;
    this.auditEventRepository = auditEventRepository;
  }

  @Transactional
  public void recordOrderPaid(String userId, long orderId, BigDecimal amount) {
    String dedupKey = "order-paid:" + orderId;
    if (notificationRepository.findByDedupKey(dedupKey).isPresent()) {
      return;
    }
    notificationRepository.save(
        new NotificationEntity(
            userId,
            "ORDER_PAID",
            "Order " + orderId + " paid successfully for " + amount,
            dedupKey));
    auditEventRepository.save(
        new AuditEventEntity(
            "notification.order_paid", userId, "Notification created for order " + orderId));
  }
}
