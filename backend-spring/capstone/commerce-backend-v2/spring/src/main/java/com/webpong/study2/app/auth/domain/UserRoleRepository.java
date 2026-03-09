package com.webpong.study2.app.auth.domain;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRoleRepository extends JpaRepository<UserRoleEntity, Long> {
  List<UserRoleEntity> findByUserId(String userId);

  boolean existsByUserIdAndRoleName(String userId, String roleName);
}
