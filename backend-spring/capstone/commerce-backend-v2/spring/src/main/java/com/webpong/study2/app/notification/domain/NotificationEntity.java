package com.webpong.study2.app.notification.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "notifications")
public class NotificationEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String userId;

  @Column(nullable = false)
  private String type;

  @Column(nullable = false)
  private String message;

  @Column(nullable = false, unique = true)
  private String dedupKey;

  @Column(nullable = false)
  private Instant createdAt;

  protected NotificationEntity() {}

  public NotificationEntity(String userId, String type, String message, String dedupKey) {
    this.userId = userId;
    this.type = type;
    this.message = message;
    this.dedupKey = dedupKey;
    this.createdAt = Instant.now();
  }

  public Long getId() {
    return id;
  }

  public String getUserId() {
    return userId;
  }

  public String getType() {
    return type;
  }

  public String getMessage() {
    return message;
  }

  public String getDedupKey() {
    return dedupKey;
  }
}
