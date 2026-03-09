package com.webpong.study2.app.auth.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "oauth_accounts")
public class OAuthAccountEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String userId;

  @Column(nullable = false)
  private String provider;

  @Column(nullable = false)
  private String providerSubject;

  @Column(nullable = false)
  private Instant createdAt;

  protected OAuthAccountEntity() {}

  public OAuthAccountEntity(String userId, String provider, String providerSubject) {
    this.userId = userId;
    this.provider = provider;
    this.providerSubject = providerSubject;
    this.createdAt = Instant.now();
  }

  public String getUserId() {
    return userId;
  }

  public String getProvider() {
    return provider;
  }

  public String getProviderSubject() {
    return providerSubject;
  }
}
