package com.webpong.study2.app.auth.infrastructure;

import com.webpong.study2.app.global.config.AuthProperties;
import com.webpong.study2.app.global.error.UnauthorizedException;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Component;

@Component
public class OAuthStateStore {

  private final Map<String, StateSnapshot> states = new ConcurrentHashMap<>();
  private final AuthProperties authProperties;

  public OAuthStateStore(AuthProperties authProperties) {
    this.authProperties = authProperties;
  }

  public AuthorizationState issue() {
    String state = UUID.randomUUID().toString();
    String nonce = UUID.randomUUID().toString();
    states.put(
        state,
        new StateSnapshot(nonce, Instant.now().plusSeconds(authProperties.oauthStateTtlSeconds())));
    return new AuthorizationState(state, nonce);
  }

  public void validate(String state, String nonce) {
    StateSnapshot snapshot = states.remove(state);
    if (snapshot == null
        || snapshot.expiresAt().isBefore(Instant.now())
        || !snapshot.nonce().equals(nonce)) {
      throw new UnauthorizedException("Invalid OAuth state");
    }
  }

  public record AuthorizationState(String state, String nonce) {}

  private record StateSnapshot(String nonce, Instant expiresAt) {}
}
