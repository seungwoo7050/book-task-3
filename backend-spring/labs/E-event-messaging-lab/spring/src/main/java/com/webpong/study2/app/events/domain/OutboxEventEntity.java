package com.webpong.study2.app.events.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "outbox_events")
public class OutboxEventEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String aggregateType;
  private String aggregateId;
  private String eventType;
  private String payload;
  private String status;

  protected OutboxEventEntity() {}

  public OutboxEventEntity(
      String aggregateType, String aggregateId, String eventType, String payload, String status) {
    this.aggregateType = aggregateType;
    this.aggregateId = aggregateId;
    this.eventType = eventType;
    this.payload = payload;
    this.status = status;
  }

  public Long getId() {
    return id;
  }

  public String getAggregateType() {
    return aggregateType;
  }

  public String getAggregateId() {
    return aggregateId;
  }

  public String getEventType() {
    return eventType;
  }

  public String getPayload() {
    return payload;
  }

  public String getStatus() {
    return status;
  }

  public void markPublished() {
    this.status = "PUBLISHED";
  }
}
