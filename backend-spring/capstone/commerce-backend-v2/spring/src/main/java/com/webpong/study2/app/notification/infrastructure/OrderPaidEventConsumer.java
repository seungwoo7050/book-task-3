package com.webpong.study2.app.notification.infrastructure;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.global.config.MessagingProperties;
import com.webpong.study2.app.notification.application.NotificationService;
import java.math.BigDecimal;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(prefix = "app.features", name = "messaging-enabled", havingValue = "true")
public class OrderPaidEventConsumer {

  private final ObjectMapper objectMapper;
  private final NotificationService notificationService;
  private final MessagingProperties messagingProperties;

  public OrderPaidEventConsumer(
      ObjectMapper objectMapper,
      NotificationService notificationService,
      MessagingProperties messagingProperties) {
    this.objectMapper = objectMapper;
    this.notificationService = notificationService;
    this.messagingProperties = messagingProperties;
  }

  @KafkaListener(topics = "${app.messaging.order-paid-topic}", groupId = "commerce-backend-v2")
  public void consume(String payload) throws Exception {
    OrderPaidMessage message = objectMapper.readValue(payload, OrderPaidMessage.class);
    if (!messagingProperties.orderPaidTopic().equals(message.topic())) {
      return;
    }
    notificationService.recordOrderPaid(message.userId(), message.orderId(), message.amount());
  }

  public record OrderPaidMessage(String topic, Long orderId, String userId, BigDecimal amount) {}
}
