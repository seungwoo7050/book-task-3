package com.webpong.study2.app.auth.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "users")
public class UserEntity {

  @Id private String id;

  @Column(nullable = false, unique = true)
  private String email;

  @Column(nullable = true)
  private String passwordHash;

  @Column(nullable = false)
  private String displayName;

  @Column(nullable = false)
  private boolean enabled;

  @Column(nullable = false)
  private Instant createdAt;

  protected UserEntity() {}

  public UserEntity(String id, String email, String passwordHash, String displayName) {
    this.id = id;
    this.email = email;
    this.passwordHash = passwordHash;
    this.displayName = displayName;
    this.enabled = true;
    this.createdAt = Instant.now();
  }

  public String getId() {
    return id;
  }

  public String getEmail() {
    return email;
  }

  public String getPasswordHash() {
    return passwordHash;
  }

  public String getDisplayName() {
    return displayName;
  }

  public boolean isEnabled() {
    return enabled;
  }

  public Instant getCreatedAt() {
    return createdAt;
  }

  public void updateDisplayName(String displayName) {
    this.displayName = displayName;
  }
}
