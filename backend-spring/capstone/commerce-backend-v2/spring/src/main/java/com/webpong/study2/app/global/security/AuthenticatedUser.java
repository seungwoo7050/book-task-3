package com.webpong.study2.app.global.security;

import java.util.List;

public record AuthenticatedUser(String userId, String email, List<String> roles) {

  public boolean hasRole(String role) {
    return roles.contains(role);
  }
}
