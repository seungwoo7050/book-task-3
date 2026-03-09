package com.webpong.study2.app.auth.infrastructure;

import com.webpong.study2.app.global.config.AuthProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.List;
import javax.crypto.SecretKey;
import org.springframework.stereotype.Component;

@Component
public class JwtService {

  private final SecretKey secretKey;
  private final AuthProperties authProperties;

  public JwtService(AuthProperties authProperties) {
    this.authProperties = authProperties;
    this.secretKey =
        Keys.hmacShaKeyFor(authProperties.jwtSecret().getBytes(StandardCharsets.UTF_8));
  }

  public String createAccessToken(String userId, String email, List<String> roles) {
    Instant now = Instant.now();
    return Jwts.builder()
        .subject(userId)
        .claim("email", email)
        .claim("roles", roles)
        .issuedAt(Date.from(now))
        .expiration(Date.from(now.plusSeconds(authProperties.accessTokenSeconds())))
        .signWith(secretKey, SignatureAlgorithm.HS256)
        .compact();
  }

  @SuppressWarnings("unchecked")
  public JwtClaims parse(String token) {
    Claims claims =
        Jwts.parser().verifyWith(secretKey).build().parseSignedClaims(token).getPayload();
    return new JwtClaims(
        claims.getSubject(), claims.get("email", String.class), (List<String>) claims.get("roles"));
  }

  public record JwtClaims(String userId, String email, List<String> roles) {}
}
