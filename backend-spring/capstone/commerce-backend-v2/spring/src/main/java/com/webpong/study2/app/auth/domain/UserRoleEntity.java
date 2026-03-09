package com.webpong.study2.app.auth.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "user_roles")
public class UserRoleEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String userId;

  @Column(nullable = false)
  private String roleName;

  @Column(nullable = false)
  private Instant createdAt;

  protected UserRoleEntity() {}

  public UserRoleEntity(String userId, String roleName) {
    this.userId = userId;
    this.roleName = roleName;
    this.createdAt = Instant.now();
  }

  public Long getId() {
    return id;
  }

  public String getUserId() {
    return userId;
  }

  public String getRoleName() {
    return roleName;
  }

  public Instant getCreatedAt() {
    return createdAt;
  }
}
