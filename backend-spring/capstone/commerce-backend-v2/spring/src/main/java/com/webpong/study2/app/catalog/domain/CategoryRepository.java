package com.webpong.study2.app.catalog.domain;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<CategoryEntity, Long> {

  boolean existsBySlug(String slug);

  Optional<CategoryEntity> findBySlug(String slug);
}
