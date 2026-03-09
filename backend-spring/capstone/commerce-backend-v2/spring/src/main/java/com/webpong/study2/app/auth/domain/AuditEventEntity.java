package com.webpong.study2.app.auth.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "audit_events")
public class AuditEventEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String eventType;

  @Column(name = "user_id", nullable = true)
  private String actorUserId;

  @Column(name = "message", nullable = false, length = 1000)
  private String detail;

  @Column(nullable = false)
  private Instant createdAt;

  protected AuditEventEntity() {}

  public AuditEventEntity(String eventType, String actorUserId, String detail) {
    this.eventType = eventType;
    this.actorUserId = actorUserId;
    this.detail = detail;
    this.createdAt = Instant.now();
  }

  public Long getId() {
    return id;
  }

  public String getEventType() {
    return eventType;
  }

  public String getActorUserId() {
    return actorUserId;
  }

  public String getDetail() {
    return detail;
  }
}
