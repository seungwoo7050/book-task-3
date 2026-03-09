package com.webpong.study2.app.auth.domain;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OAuthAccountRepository extends JpaRepository<OAuthAccountEntity, Long> {
  Optional<OAuthAccountEntity> findByProviderAndProviderSubject(
      String provider, String providerSubject);
}
