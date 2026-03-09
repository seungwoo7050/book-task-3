package com.webpong.study2.app.catalog.api;

import com.webpong.study2.app.catalog.application.CatalogService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin/products")
public class AdminProductController {

  private final CatalogService catalogService;

  public AdminProductController(CatalogService catalogService) {
    this.catalogService = catalogService;
  }

  @PostMapping
  @ResponseStatus(HttpStatus.CREATED)
  public CatalogService.ProductDetails createProduct(@Valid @RequestBody ProductRequest request) {
    return catalogService.createProduct(
        request.categoryId(),
        request.name(),
        request.description(),
        request.price(),
        request.stock());
  }

  @PutMapping("/{productId}")
  public CatalogService.ProductDetails updateProduct(
      @PathVariable long productId, @Valid @RequestBody UpdateProductRequest request) {
    return catalogService.updateProduct(
        productId,
        request.categoryId(),
        request.name(),
        request.description(),
        request.price(),
        request.stock(),
        request.active());
  }

  @PostMapping("/{productId}/deactivate")
  public CatalogService.ProductDetails deactivateProduct(@PathVariable long productId) {
    return catalogService.deactivateProduct(productId);
  }

  public record ProductRequest(
      @NotNull Long categoryId,
      @NotBlank String name,
      @NotBlank String description,
      @DecimalMin("0.01") BigDecimal price,
      @Min(0) int stock) {}

  public record UpdateProductRequest(
      @NotNull Long categoryId,
      @NotBlank String name,
      @NotBlank String description,
      @DecimalMin("0.01") BigDecimal price,
      @Min(0) int stock,
      boolean active) {}
}
