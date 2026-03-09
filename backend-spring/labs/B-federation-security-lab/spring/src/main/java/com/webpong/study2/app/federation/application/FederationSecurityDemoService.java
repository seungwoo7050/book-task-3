package com.webpong.study2.app.federation.application;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;

@Service
public class FederationSecurityDemoService {

  private final Map<String, String> linkedIdentities = new ConcurrentHashMap<>();
  private final Map<String, String> totpSecrets = new ConcurrentHashMap<>();
  private final List<AuditEvent> auditEvents = new ArrayList<>();

  public AuthorizationUrl authorize() {
    String state = UUID.randomUUID().toString();
    String nonce = UUID.randomUUID().toString();
    auditEvents.add(new AuditEvent("google_authorize", "generated state=" + state));
    return new AuthorizationUrl(
        "https://accounts.google.com/o/oauth2/v2/auth?state=" + state + "&nonce=" + nonce,
        state,
        nonce);
  }

  public LinkedIdentity callback(String email, String subject) {
    linkedIdentities.put(email, subject);
    auditEvents.add(new AuditEvent("google_callback", email));
    return new LinkedIdentity(email, "google", subject);
  }

  public TotpSetup setupTotp(String email) {
    String secret = UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
    String expectedCode = secret.substring(0, 6);
    totpSecrets.put(email, expectedCode);
    auditEvents.add(new AuditEvent("totp_setup", email));
    return new TotpSetup(secret, List.of("rec-1", "rec-2", "rec-3"), expectedCode);
  }

  public VerificationResult verifyTotp(String email, String code) {
    boolean verified = code.equals(totpSecrets.get(email));
    auditEvents.add(new AuditEvent("totp_verify", email + ":" + verified));
    return new VerificationResult(verified);
  }

  public List<AuditEvent> auditEvents() {
    return List.copyOf(auditEvents);
  }

  public record AuthorizationUrl(String url, String state, String nonce) {}

  public record LinkedIdentity(String email, String provider, String subject) {}

  public record TotpSetup(String secret, List<String> recoveryCodes, String expectedCode) {}

  public record VerificationResult(boolean verified) {}

  public record AuditEvent(String type, String detail) {}
}
