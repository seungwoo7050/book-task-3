package com.webpong.study2.app.authorization.api;

import com.webpong.study2.app.authorization.application.AuthorizationDemoService;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1")
public class AuthorizationController {

  private final AuthorizationDemoService service;

  public AuthorizationController(AuthorizationDemoService service) {
    this.service = service;
  }

  @PostMapping("/organizations")
  public AuthorizationDemoService.Organization createOrganization(
      @RequestBody OrganizationRequest request) {
    return service.createOrganization(request.name(), request.ownerEmail());
  }

  @PostMapping("/organizations/{organizationId}/invites")
  public AuthorizationDemoService.Invitation invite(
      @PathVariable long organizationId, @RequestBody InviteRequest request) {
    return service.invite(organizationId, request.email(), request.role());
  }

  @PostMapping("/invitations/{invitationId}/accept")
  public AuthorizationDemoService.Membership accept(@PathVariable long invitationId) {
    return service.accept(invitationId);
  }

  @PatchMapping("/organizations/{organizationId}/members/{email}/role")
  public AuthorizationDemoService.Membership changeRole(
      @PathVariable long organizationId,
      @PathVariable String email,
      @RequestBody RoleRequest request) {
    return service.changeRole(organizationId, email, request.role());
  }

  public record OrganizationRequest(@NotBlank String name, @Email String ownerEmail) {}

  public record InviteRequest(@Email String email, @NotBlank String role) {}

  public record RoleRequest(@NotBlank String role) {}
}
