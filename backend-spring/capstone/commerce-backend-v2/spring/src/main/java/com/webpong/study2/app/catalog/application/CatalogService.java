package com.webpong.study2.app.catalog.application;

import com.webpong.study2.app.catalog.domain.CategoryEntity;
import com.webpong.study2.app.catalog.domain.CategoryRepository;
import com.webpong.study2.app.catalog.domain.ProductEntity;
import com.webpong.study2.app.catalog.domain.ProductRepository;
import com.webpong.study2.app.global.api.PageResponse;
import com.webpong.study2.app.global.error.ConflictException;
import com.webpong.study2.app.global.error.NotFoundException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CatalogService {

  private final CategoryRepository categoryRepository;
  private final ProductRepository productRepository;

  public CatalogService(
      CategoryRepository categoryRepository, ProductRepository productRepository) {
    this.categoryRepository = categoryRepository;
    this.productRepository = productRepository;
  }

  @Transactional(readOnly = true)
  public PageResponse<ProductSummary> listProducts(int page, int size, String sort) {
    Page<ProductSummary> products =
        productRepository.findByActiveTrue(buildPageable(page, size, sort)).map(this::toSummary);
    return PageResponse.from(products);
  }

  @Transactional(readOnly = true)
  public ProductDetails getProduct(long productId) {
    ProductEntity product = requireProduct(productId);
    return toDetails(product, requireCategory(product.getCategoryId()));
  }

  @Transactional
  public CategoryResponse createCategory(String name, String slug) {
    if (categoryRepository.existsBySlug(slug)) {
      throw new ConflictException("Category slug already exists");
    }
    return toCategoryResponse(categoryRepository.save(new CategoryEntity(name, slug)));
  }

  @Transactional
  public CategoryResponse updateCategory(
      long categoryId, String name, String slug, boolean active) {
    CategoryEntity category = requireCategory(categoryId);
    categoryRepository
        .findBySlug(slug)
        .filter(existing -> !existing.getId().equals(categoryId))
        .ifPresent(
            existing -> {
              throw new ConflictException("Category slug already exists");
            });
    category.update(name, slug, active);
    return toCategoryResponse(category);
  }

  @Transactional
  public ProductDetails createProduct(
      long categoryId, String name, String description, BigDecimal price, int stock) {
    CategoryEntity category = requireCategory(categoryId);
    ProductEntity product =
        productRepository.save(
            new ProductEntity(category.getId(), name, description, normalize(price), stock));
    return toDetails(product, category);
  }

  @Transactional
  public ProductDetails updateProduct(
      long productId,
      long categoryId,
      String name,
      String description,
      BigDecimal price,
      int stock,
      boolean active) {
    CategoryEntity category = requireCategory(categoryId);
    ProductEntity product = requireProduct(productId);
    product.update(category.getId(), name, description, normalize(price), stock, active);
    return toDetails(product, category);
  }

  @Transactional
  public ProductDetails deactivateProduct(long productId) {
    ProductEntity product = requireProduct(productId);
    product.deactivate();
    return toDetails(product, requireCategory(product.getCategoryId()));
  }

  @Transactional(readOnly = true)
  public CategoryEntity requireCategory(long categoryId) {
    return categoryRepository
        .findById(categoryId)
        .orElseThrow(() -> new NotFoundException("Category not found"));
  }

  @Transactional(readOnly = true)
  public ProductEntity requireProduct(long productId) {
    return productRepository
        .findById(productId)
        .orElseThrow(() -> new NotFoundException("Product not found"));
  }

  private Pageable buildPageable(int page, int size, String sort) {
    String[] tokens = sort.split(",");
    String property =
        switch (tokens[0]) {
          case "price", "name", "createdAt" -> tokens[0];
          default -> "id";
        };
    Sort.Direction direction =
        tokens.length > 1 && "asc".equalsIgnoreCase(tokens[1])
            ? Sort.Direction.ASC
            : Sort.Direction.DESC;
    return PageRequest.of(
        Math.max(page, 0), Math.min(Math.max(size, 1), 50), Sort.by(direction, property));
  }

  private BigDecimal normalize(BigDecimal price) {
    return price.setScale(2, RoundingMode.HALF_UP);
  }

  private ProductSummary toSummary(ProductEntity product) {
    return new ProductSummary(
        product.getId(),
        product.getCategoryId(),
        product.getName(),
        product.getPrice(),
        product.getStock(),
        product.isActive());
  }

  private ProductDetails toDetails(ProductEntity product, CategoryEntity category) {
    return new ProductDetails(
        product.getId(),
        category.getId(),
        category.getName(),
        category.getSlug(),
        product.getName(),
        product.getDescription(),
        product.getPrice(),
        product.getStock(),
        product.isActive(),
        product.getVersion());
  }

  private CategoryResponse toCategoryResponse(CategoryEntity category) {
    return new CategoryResponse(
        category.getId(), category.getName(), category.getSlug(), category.isActive());
  }

  public record CategoryResponse(Long id, String name, String slug, boolean active) {}

  public record ProductSummary(
      Long id, Long categoryId, String name, BigDecimal price, int stock, boolean active) {}

  public record ProductDetails(
      Long id,
      Long categoryId,
      String categoryName,
      String categorySlug,
      String name,
      String description,
      BigDecimal price,
      int stock,
      boolean active,
      Long version) {}
}
