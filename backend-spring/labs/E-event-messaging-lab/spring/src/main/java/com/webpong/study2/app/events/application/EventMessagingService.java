package com.webpong.study2.app.events.application;

import com.webpong.study2.app.events.domain.OutboxEventEntity;
import com.webpong.study2.app.events.domain.OutboxEventRepository;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class EventMessagingService {

  private final OutboxEventRepository outboxEventRepository;

  public EventMessagingService(OutboxEventRepository outboxEventRepository) {
    this.outboxEventRepository = outboxEventRepository;
  }

  @Transactional
  public EventResponse emitOrderPlaced(String orderId) {
    OutboxEventEntity entity =
        outboxEventRepository.save(
            new OutboxEventEntity(
                "ORDER", orderId, "ORDER_PLACED", "{\"orderId\":\"" + orderId + "\"}", "PENDING"));
    return EventResponse.from(entity);
  }

  @Transactional
  public List<EventResponse> publishPending() {
    List<OutboxEventEntity> pending = outboxEventRepository.findByStatus("PENDING");
    pending.forEach(OutboxEventEntity::markPublished);
    return pending.stream().map(EventResponse::from).toList();
  }

  @Transactional(readOnly = true)
  public List<EventResponse> list() {
    return outboxEventRepository.findAll().stream().map(EventResponse::from).toList();
  }

  public record EventResponse(
      Long id, String aggregateType, String aggregateId, String eventType, String status) {
    public static EventResponse from(OutboxEventEntity entity) {
      return new EventResponse(
          entity.getId(),
          entity.getAggregateType(),
          entity.getAggregateId(),
          entity.getEventType(),
          entity.getStatus());
    }
  }
}
