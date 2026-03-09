package com.webpong.study2.app.data.application;

import com.webpong.study2.app.data.domain.ProductEntity;
import com.webpong.study2.app.data.domain.ProductRepository;
import java.math.BigDecimal;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class DataApiService {

  private final ProductRepository productRepository;

  public DataApiService(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @Transactional
  public ProductResponse create(String name, BigDecimal price) {
    ProductEntity saved = productRepository.save(new ProductEntity(name, price));
    return ProductResponse.from(saved);
  }

  @Transactional(readOnly = true)
  public PageEnvelope<ProductResponse> list(int page, int size) {
    Page<ProductResponse> products =
        productRepository.findAll(PageRequest.of(page, size)).map(ProductResponse::from);
    return new PageEnvelope<>(
        products.getContent(),
        products.getNumber(),
        products.getSize(),
        products.getTotalElements(),
        products.getTotalPages(),
        products.hasNext());
  }

  @Transactional
  public ProductResponse updatePrice(long productId, long version, BigDecimal price) {
    ProductEntity product =
        productRepository
            .findById(productId)
            .orElseThrow(() -> new IllegalArgumentException("Product not found"));
    if (product.getVersion() != version) {
      throw new IllegalArgumentException("Version conflict");
    }
    product.changePrice(price);
    return ProductResponse.from(product);
  }

  public record ProductResponse(Long id, String name, BigDecimal price, long version) {
    public static ProductResponse from(ProductEntity entity) {
      return new ProductResponse(
          entity.getId(), entity.getName(), entity.getPrice(), entity.getVersion());
    }
  }

  public record PageEnvelope<T>(
      java.util.List<T> content,
      int page,
      int size,
      long totalElements,
      int totalPages,
      boolean hasNext) {}
}
