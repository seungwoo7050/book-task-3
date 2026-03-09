package com.webpong.study2.app.global.security;

import com.webpong.study2.app.global.error.ForbiddenException;
import com.webpong.study2.app.global.error.UnauthorizedException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class AuthenticationFacade {

  public AuthenticatedUser currentUser() {
    Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    if (authentication == null
        || !(authentication.getPrincipal() instanceof AuthenticatedUser user)) {
      throw new UnauthorizedException("Authentication is required");
    }
    return user;
  }

  public AuthenticatedUser requireAdmin() {
    AuthenticatedUser user = currentUser();
    if (!user.hasRole("ADMIN")) {
      throw new ForbiddenException("Admin role is required");
    }
    return user;
  }
}
