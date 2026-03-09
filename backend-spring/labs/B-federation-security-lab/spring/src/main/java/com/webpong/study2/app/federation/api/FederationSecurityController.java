package com.webpong.study2.app.federation.api;

import com.webpong.study2.app.federation.application.FederationSecurityDemoService;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1")
public class FederationSecurityController {

  private final FederationSecurityDemoService service;

  public FederationSecurityController(FederationSecurityDemoService service) {
    this.service = service;
  }

  @GetMapping("/auth/google/authorize")
  public FederationSecurityDemoService.AuthorizationUrl authorize() {
    return service.authorize();
  }

  @PostMapping("/auth/google/callback")
  public FederationSecurityDemoService.LinkedIdentity callback(
      @RequestBody CallbackRequest request) {
    return service.callback(request.email(), request.subject());
  }

  @PostMapping("/auth/2fa/setup")
  public FederationSecurityDemoService.TotpSetup setup(@RequestBody EmailRequest request) {
    return service.setupTotp(request.email());
  }

  @PostMapping("/auth/2fa/verify")
  public FederationSecurityDemoService.VerificationResult verify(
      @RequestBody VerifyRequest request) {
    return service.verifyTotp(request.email(), request.code());
  }

  @GetMapping("/audit-events")
  public Object auditEvents() {
    return service.auditEvents();
  }

  public record CallbackRequest(@Email String email, @NotBlank String subject) {}

  public record EmailRequest(@Email String email) {}

  public record VerifyRequest(@Email String email, @NotBlank String code) {}
}
