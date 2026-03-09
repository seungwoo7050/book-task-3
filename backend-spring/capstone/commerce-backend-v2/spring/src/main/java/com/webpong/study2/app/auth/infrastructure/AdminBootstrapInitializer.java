package com.webpong.study2.app.auth.infrastructure;

import com.webpong.study2.app.auth.domain.UserEntity;
import com.webpong.study2.app.auth.domain.UserRepository;
import com.webpong.study2.app.auth.domain.UserRoleEntity;
import com.webpong.study2.app.auth.domain.UserRoleRepository;
import com.webpong.study2.app.global.config.BootstrapAdminProperties;
import java.util.UUID;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class AdminBootstrapInitializer implements ApplicationRunner {

  private final UserRepository userRepository;
  private final UserRoleRepository userRoleRepository;
  private final PasswordEncoder passwordEncoder;
  private final BootstrapAdminProperties bootstrapAdminProperties;

  public AdminBootstrapInitializer(
      UserRepository userRepository,
      UserRoleRepository userRoleRepository,
      PasswordEncoder passwordEncoder,
      BootstrapAdminProperties bootstrapAdminProperties) {
    this.userRepository = userRepository;
    this.userRoleRepository = userRoleRepository;
    this.passwordEncoder = passwordEncoder;
    this.bootstrapAdminProperties = bootstrapAdminProperties;
  }

  @Override
  public void run(ApplicationArguments args) {
    userRepository
        .findByEmail(bootstrapAdminProperties.email())
        .ifPresentOrElse(
            existing -> ensureAdminRole(existing.getId()),
            () -> {
              UserEntity admin =
                  userRepository.save(
                      new UserEntity(
                          UUID.randomUUID().toString(),
                          bootstrapAdminProperties.email(),
                          passwordEncoder.encode(bootstrapAdminProperties.password()),
                          bootstrapAdminProperties.displayName()));
              ensureAdminRole(admin.getId());
            });
  }

  private void ensureAdminRole(String userId) {
    if (!userRoleRepository.existsByUserIdAndRoleName(userId, "ADMIN")) {
      userRoleRepository.save(new UserRoleEntity(userId, "ADMIN"));
    }
  }
}
