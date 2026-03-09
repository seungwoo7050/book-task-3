package com.webpong.study2.app.authorization.application;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

@Service
public class AuthorizationDemoService {

  private final AtomicLong organizationSequence = new AtomicLong(1);
  private final AtomicLong invitationSequence = new AtomicLong(1);
  private final Map<Long, Organization> organizations = new ConcurrentHashMap<>();
  private final Map<Long, Invitation> invitations = new ConcurrentHashMap<>();

  public Organization createOrganization(String name, String ownerEmail) {
    long id = organizationSequence.getAndIncrement();
    Organization organization = new Organization(id, name, new ConcurrentHashMap<>());
    organization.members().put(ownerEmail, "OWNER");
    organizations.put(id, organization);
    return organization;
  }

  public Invitation invite(long organizationId, String email, String role) {
    Organization organization = requireOrganization(organizationId);
    long invitationId = invitationSequence.getAndIncrement();
    Invitation invitation =
        new Invitation(
            invitationId, organizationId, email, role, UUID.randomUUID().toString(), false);
    invitations.put(invitationId, invitation);
    organization.members().putIfAbsent(email, "PENDING");
    return invitation;
  }

  public Membership accept(long invitationId) {
    Invitation invitation = requireInvitation(invitationId);
    invitations.put(
        invitationId,
        new Invitation(
            invitation.id(),
            invitation.organizationId(),
            invitation.email(),
            invitation.role(),
            invitation.token(),
            true));
    Organization organization = requireOrganization(invitation.organizationId());
    organization.members().put(invitation.email(), invitation.role());
    return new Membership(invitation.organizationId(), invitation.email(), invitation.role());
  }

  public Membership changeRole(long organizationId, String email, String role) {
    Organization organization = requireOrganization(organizationId);
    if (!organization.members().containsKey(email)) {
      throw new IllegalArgumentException("Member not found");
    }
    organization.members().put(email, role);
    return new Membership(organizationId, email, role);
  }

  private Organization requireOrganization(long organizationId) {
    Organization organization = organizations.get(organizationId);
    if (organization == null) {
      throw new IllegalArgumentException("Organization not found");
    }
    return organization;
  }

  private Invitation requireInvitation(long invitationId) {
    Invitation invitation = invitations.get(invitationId);
    if (invitation == null) {
      throw new IllegalArgumentException("Invitation not found");
    }
    return invitation;
  }

  public record Organization(long id, String name, Map<String, String> members) {}

  public record Invitation(
      long id, long organizationId, String email, String role, String token, boolean accepted) {}

  public record Membership(long organizationId, String email, String role) {}
}
