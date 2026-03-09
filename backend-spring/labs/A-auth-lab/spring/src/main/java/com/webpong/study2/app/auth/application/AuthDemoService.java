package com.webpong.study2.app.auth.application;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;

@Service
public class AuthDemoService {

  private final Map<String, UserProfile> users = new ConcurrentHashMap<>();
  private final Map<String, SessionSnapshot> sessions = new ConcurrentHashMap<>();

  public RegisterResult register(String email, String password) {
    if (users.containsKey(email)) {
      throw new IllegalArgumentException("Account already exists");
    }

    UserProfile profile =
        new UserProfile(UUID.randomUUID().toString(), email, "bcrypt$" + password, false);
    users.put(email, profile);
    return new RegisterResult(profile.userId(), email, UUID.randomUUID().toString());
  }

  public SessionSnapshot login(String email, String password) {
    UserProfile profile = requireUser(email);
    if (!profile.passwordHash().equals("bcrypt$" + password)) {
      throw new IllegalArgumentException("Invalid credentials");
    }

    SessionSnapshot session =
        new SessionSnapshot(
            profile.userId(),
            profile.email(),
            "access-" + UUID.randomUUID(),
            "refresh-" + UUID.randomUUID(),
            "csrf-" + UUID.randomUUID());
    sessions.put(session.refreshToken(), session);
    return session;
  }

  public SessionSnapshot refresh(String refreshToken, String csrfToken) {
    SessionSnapshot existing = requireSession(refreshToken, csrfToken);
    sessions.remove(refreshToken);
    SessionSnapshot rotated =
        new SessionSnapshot(
            existing.userId(),
            existing.email(),
            "access-" + UUID.randomUUID(),
            "refresh-" + UUID.randomUUID(),
            "csrf-" + UUID.randomUUID());
    sessions.put(rotated.refreshToken(), rotated);
    return rotated;
  }

  public void logout(String refreshToken, String csrfToken) {
    requireSession(refreshToken, csrfToken);
    sessions.remove(refreshToken);
  }

  public UserProfile me(String email) {
    return requireUser(email);
  }

  private UserProfile requireUser(String email) {
    UserProfile profile = users.get(email);
    if (profile == null) {
      throw new IllegalArgumentException("Account not found");
    }
    return profile;
  }

  private SessionSnapshot requireSession(String refreshToken, String csrfToken) {
    SessionSnapshot session = sessions.get(refreshToken);
    if (session == null) {
      throw new IllegalArgumentException("Refresh token not found");
    }
    if (!session.csrfToken().equals(csrfToken)) {
      throw new IllegalArgumentException("CSRF token mismatch");
    }
    return session;
  }

  public record RegisterResult(String userId, String email, String verificationToken) {}

  public record SessionSnapshot(
      String userId, String email, String accessToken, String refreshToken, String csrfToken) {}

  public record UserProfile(String userId, String email, String passwordHash, boolean verified) {}
}
