package com.webpong.study2.app.catalog.api;

import com.webpong.study2.app.catalog.application.CatalogService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin/categories")
public class AdminCategoryController {

  private final CatalogService catalogService;

  public AdminCategoryController(CatalogService catalogService) {
    this.catalogService = catalogService;
  }

  @PostMapping
  @ResponseStatus(HttpStatus.CREATED)
  public CatalogService.CategoryResponse createCategory(
      @Valid @RequestBody CategoryRequest request) {
    return catalogService.createCategory(request.name(), request.slug());
  }

  @PutMapping("/{categoryId}")
  public CatalogService.CategoryResponse updateCategory(
      @PathVariable long categoryId, @Valid @RequestBody UpdateCategoryRequest request) {
    return catalogService.updateCategory(
        categoryId, request.name(), request.slug(), request.active());
  }

  public record CategoryRequest(@NotBlank String name, @NotBlank String slug) {}

  public record UpdateCategoryRequest(
      @NotBlank String name, @NotBlank String slug, boolean active) {}
}
