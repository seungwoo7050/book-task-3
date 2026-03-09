package com.webpong.study2.app.auth.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "refresh_tokens")
public class RefreshTokenEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false, unique = true, length = 128)
  private String tokenHash;

  @Column(nullable = false)
  private String userId;

  @Column(nullable = false)
  private String csrfToken;

  @Column(nullable = false)
  private Instant expiresAt;

  @Column(nullable = false)
  private boolean revoked;

  @Column(nullable = false)
  private Instant createdAt;

  protected RefreshTokenEntity() {}

  public RefreshTokenEntity(String tokenHash, String userId, String csrfToken, Instant expiresAt) {
    this.tokenHash = tokenHash;
    this.userId = userId;
    this.csrfToken = csrfToken;
    this.expiresAt = expiresAt;
    this.revoked = false;
    this.createdAt = Instant.now();
  }

  public String getTokenHash() {
    return tokenHash;
  }

  public String getUserId() {
    return userId;
  }

  public String getCsrfToken() {
    return csrfToken;
  }

  public Instant getExpiresAt() {
    return expiresAt;
  }

  public boolean isRevoked() {
    return revoked;
  }

  public void revoke() {
    this.revoked = true;
  }
}
