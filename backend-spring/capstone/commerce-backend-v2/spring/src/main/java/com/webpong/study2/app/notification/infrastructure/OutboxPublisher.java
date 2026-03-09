package com.webpong.study2.app.notification.infrastructure;

import com.webpong.study2.app.notification.domain.OutboxEventEntity;
import com.webpong.study2.app.notification.domain.OutboxEventRepository;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(prefix = "app.features", name = "messaging-enabled", havingValue = "true")
public class OutboxPublisher {

  private final OutboxEventRepository outboxEventRepository;
  private final KafkaTemplate<String, String> kafkaTemplate;

  public OutboxPublisher(
      OutboxEventRepository outboxEventRepository, KafkaTemplate<String, String> kafkaTemplate) {
    this.outboxEventRepository = outboxEventRepository;
    this.kafkaTemplate = kafkaTemplate;
  }

  @Scheduled(fixedDelayString = "${app.messaging.publish-delay-ms}")
  public void publishPending() {
    List<OutboxEventEntity> events =
        outboxEventRepository.findTop20ByPublishedAtIsNullOrderByIdAsc();
    for (OutboxEventEntity event : events) {
      try {
        kafkaTemplate
            .send(event.getEventType(), event.getAggregateId(), event.getPayload())
            .get(5, TimeUnit.SECONDS);
        event.markPublished();
      } catch (Exception exception) {
        return;
      }
    }
  }
}
