package com.webpong.study2.app.auth.application;

import com.webpong.study2.app.auth.domain.AuditEventEntity;
import com.webpong.study2.app.auth.domain.AuditEventRepository;
import com.webpong.study2.app.auth.domain.OAuthAccountEntity;
import com.webpong.study2.app.auth.domain.OAuthAccountRepository;
import com.webpong.study2.app.auth.domain.RefreshTokenEntity;
import com.webpong.study2.app.auth.domain.RefreshTokenRepository;
import com.webpong.study2.app.auth.domain.UserEntity;
import com.webpong.study2.app.auth.domain.UserRepository;
import com.webpong.study2.app.auth.domain.UserRoleEntity;
import com.webpong.study2.app.auth.domain.UserRoleRepository;
import com.webpong.study2.app.auth.infrastructure.AttemptLimiter;
import com.webpong.study2.app.auth.infrastructure.HashingSupport;
import com.webpong.study2.app.auth.infrastructure.JwtService;
import com.webpong.study2.app.auth.infrastructure.OAuthStateStore;
import com.webpong.study2.app.global.config.AuthProperties;
import com.webpong.study2.app.global.config.RateLimitProperties;
import com.webpong.study2.app.global.error.ConflictException;
import com.webpong.study2.app.global.error.NotFoundException;
import com.webpong.study2.app.global.error.TooManyRequestsException;
import com.webpong.study2.app.global.error.UnauthorizedException;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

  private final UserRepository userRepository;
  private final UserRoleRepository userRoleRepository;
  private final RefreshTokenRepository refreshTokenRepository;
  private final OAuthAccountRepository oAuthAccountRepository;
  private final AuditEventRepository auditEventRepository;
  private final PasswordEncoder passwordEncoder;
  private final JwtService jwtService;
  private final AttemptLimiter attemptLimiter;
  private final OAuthStateStore oAuthStateStore;
  private final AuthProperties authProperties;
  private final RateLimitProperties rateLimitProperties;

  public AuthService(
      UserRepository userRepository,
      UserRoleRepository userRoleRepository,
      RefreshTokenRepository refreshTokenRepository,
      OAuthAccountRepository oAuthAccountRepository,
      AuditEventRepository auditEventRepository,
      PasswordEncoder passwordEncoder,
      JwtService jwtService,
      AttemptLimiter attemptLimiter,
      OAuthStateStore oAuthStateStore,
      AuthProperties authProperties,
      RateLimitProperties rateLimitProperties) {
    this.userRepository = userRepository;
    this.userRoleRepository = userRoleRepository;
    this.refreshTokenRepository = refreshTokenRepository;
    this.oAuthAccountRepository = oAuthAccountRepository;
    this.auditEventRepository = auditEventRepository;
    this.passwordEncoder = passwordEncoder;
    this.jwtService = jwtService;
    this.attemptLimiter = attemptLimiter;
    this.oAuthStateStore = oAuthStateStore;
    this.authProperties = authProperties;
    this.rateLimitProperties = rateLimitProperties;
  }

  @Transactional
  public AuthUserProfile register(String email, String password, String displayName) {
    if (userRepository.existsByEmail(email)) {
      throw new ConflictException("Email is already registered");
    }

    UserEntity user =
        userRepository.save(
            new UserEntity(
                UUID.randomUUID().toString(),
                email,
                passwordEncoder.encode(password),
                displayName));
    userRoleRepository.save(new UserRoleEntity(user.getId(), "CUSTOMER"));
    auditEventRepository.save(new AuditEventEntity("auth.registered", user.getId(), email));
    return requireUserProfile(user.getId());
  }

  @Transactional(readOnly = true)
  public AuthorizationUrl issueGoogleAuthorizationUrl() {
    OAuthStateStore.AuthorizationState authorizationState = oAuthStateStore.issue();
    String url =
        "https://accounts.google.com/o/oauth2/v2/auth?client_id="
            + authProperties.googleClientId()
            + "&redirect_uri="
            + authProperties.googleRedirectUri()
            + "&response_type=code&scope=openid%20email%20profile&state="
            + authorizationState.state()
            + "&nonce="
            + authorizationState.nonce();
    return new AuthorizationUrl(url, authorizationState.state(), authorizationState.nonce());
  }

  @Transactional
  public SessionSnapshot login(String email, String password) {
    enforceRateLimit(
        "login:" + email,
        rateLimitProperties.loginMaxAttempts(),
        rateLimitProperties.loginWindowSeconds());
    UserEntity user =
        userRepository
            .findByEmail(email)
            .orElseThrow(() -> new UnauthorizedException("Invalid credentials"));
    if (user.getPasswordHash() == null
        || !passwordEncoder.matches(password, user.getPasswordHash())) {
      throw new UnauthorizedException("Invalid credentials");
    }
    auditEventRepository.save(new AuditEventEntity("auth.login", user.getId(), email));
    return issueSession(user);
  }

  @Transactional
  public SessionSnapshot refresh(String refreshToken, String csrfToken) {
    enforceRateLimit(
        "refresh:" + HashingSupport.sha256(refreshToken),
        rateLimitProperties.refreshMaxAttempts(),
        rateLimitProperties.refreshWindowSeconds());
    RefreshTokenEntity stored = requireValidRefreshToken(refreshToken, csrfToken);
    stored.revoke();
    UserEntity user = requireUser(stored.getUserId());
    auditEventRepository.save(new AuditEventEntity("auth.refresh", user.getId(), user.getEmail()));
    return issueSession(user);
  }

  @Transactional
  public void logout(String refreshToken, String csrfToken) {
    RefreshTokenEntity stored = requireValidRefreshToken(refreshToken, csrfToken);
    stored.revoke();
    auditEventRepository.save(
        new AuditEventEntity("auth.logout", stored.getUserId(), "refresh token revoked"));
  }

  @Transactional
  public SessionSnapshot googleCallback(
      String state, String nonce, String email, String providerSubject, String displayName) {
    oAuthStateStore.validate(state, nonce);

    UserEntity user =
        oAuthAccountRepository
            .findByProviderAndProviderSubject("google", providerSubject)
            .map(account -> requireUser(account.getUserId()))
            .orElseGet(
                () ->
                    userRepository
                        .findByEmail(email)
                        .orElseGet(() -> registerOAuthUser(email, displayName)));

    if (oAuthAccountRepository
        .findByProviderAndProviderSubject("google", providerSubject)
        .isEmpty()) {
      oAuthAccountRepository.save(new OAuthAccountEntity(user.getId(), "google", providerSubject));
    }

    auditEventRepository.save(
        new AuditEventEntity("auth.google_callback", user.getId(), providerSubject));
    return issueSession(user);
  }

  @Transactional(readOnly = true)
  public AuthUserProfile requireUserProfile(String userId) {
    UserEntity user = requireUser(userId);
    List<String> roles =
        userRoleRepository.findByUserId(userId).stream().map(UserRoleEntity::getRoleName).toList();
    return new AuthUserProfile(user.getId(), user.getEmail(), user.getDisplayName(), roles);
  }

  @Transactional(readOnly = true)
  public AuthUserProfile me(String userId) {
    return requireUserProfile(userId);
  }

  private void enforceRateLimit(String bucket, int maxAttempts, long windowSeconds) {
    if (!attemptLimiter.allow(bucket, maxAttempts, windowSeconds)) {
      throw new TooManyRequestsException("Too many attempts");
    }
  }

  private RefreshTokenEntity requireValidRefreshToken(String refreshToken, String csrfToken) {
    RefreshTokenEntity stored =
        refreshTokenRepository
            .findByTokenHash(HashingSupport.sha256(refreshToken))
            .orElseThrow(() -> new UnauthorizedException("Refresh token is invalid"));
    if (stored.isRevoked() || stored.getExpiresAt().isBefore(Instant.now())) {
      throw new UnauthorizedException("Refresh token is invalid");
    }
    if (!stored.getCsrfToken().equals(csrfToken)) {
      throw new UnauthorizedException("CSRF token is invalid");
    }
    return stored;
  }

  private SessionSnapshot issueSession(UserEntity user) {
    AuthUserProfile profile = requireUserProfile(user.getId());
    String refreshToken = UUID.randomUUID().toString();
    String csrfToken = UUID.randomUUID().toString();
    refreshTokenRepository.save(
        new RefreshTokenEntity(
            HashingSupport.sha256(refreshToken),
            user.getId(),
            csrfToken,
            Instant.now().plusSeconds(authProperties.refreshTokenSeconds())));
    return new SessionSnapshot(
        jwtService.createAccessToken(profile.userId(), profile.email(), profile.roles()),
        refreshToken,
        csrfToken,
        profile);
  }

  private UserEntity registerOAuthUser(String email, String displayName) {
    UserEntity created =
        userRepository.save(new UserEntity(UUID.randomUUID().toString(), email, null, displayName));
    userRoleRepository.save(new UserRoleEntity(created.getId(), "CUSTOMER"));
    return created;
  }

  private UserEntity requireUser(String userId) {
    return userRepository
        .findById(userId)
        .orElseThrow(() -> new NotFoundException("User not found"));
  }

  public record AuthUserProfile(
      String userId, String email, String displayName, List<String> roles) {}

  public record SessionSnapshot(
      String accessToken, String refreshToken, String csrfToken, AuthUserProfile user) {}

  public record AuthorizationUrl(String url, String state, String nonce) {}
}
