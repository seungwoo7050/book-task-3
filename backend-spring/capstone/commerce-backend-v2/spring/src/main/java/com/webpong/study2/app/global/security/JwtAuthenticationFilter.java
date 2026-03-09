package com.webpong.study2.app.global.security;

import com.webpong.study2.app.auth.application.AuthService;
import com.webpong.study2.app.auth.infrastructure.JwtService;
import com.webpong.study2.app.global.error.UnauthorizedException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

  private final JwtService jwtService;
  private final AuthService authService;

  public JwtAuthenticationFilter(JwtService jwtService, AuthService authService) {
    this.jwtService = jwtService;
    this.authService = authService;
  }

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
      throws ServletException, IOException {
    String header = request.getHeader("Authorization");
    if (StringUtils.hasText(header) && header.startsWith("Bearer ")) {
      String token = header.substring(7);
      try {
        JwtService.JwtClaims claims = jwtService.parse(token);
        AuthService.AuthUserProfile profile = authService.requireUserProfile(claims.userId());
        AuthenticatedUser authenticatedUser =
            new AuthenticatedUser(profile.userId(), profile.email(), profile.roles());
        List<SimpleGrantedAuthority> authorities =
            profile.roles().stream()
                .map(role -> new SimpleGrantedAuthority("ROLE_" + role))
                .toList();
        UsernamePasswordAuthenticationToken authentication =
            new UsernamePasswordAuthenticationToken(authenticatedUser, token, authorities);
        SecurityContextHolder.getContext().setAuthentication(authentication);
      } catch (RuntimeException exception) {
        SecurityContextHolder.clearContext();
        throw new UnauthorizedException("Invalid access token");
      }
    }

    filterChain.doFilter(request, response);
  }
}
