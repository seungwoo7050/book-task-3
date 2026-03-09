package com.webpong.study2.app.catalog.api;

import com.webpong.study2.app.catalog.application.CatalogService;
import com.webpong.study2.app.global.api.PageResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/products")
public class CatalogController {

  private final CatalogService catalogService;

  public CatalogController(CatalogService catalogService) {
    this.catalogService = catalogService;
  }

  @GetMapping
  public PageResponse<CatalogService.ProductSummary> listProducts(
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "20") int size,
      @RequestParam(defaultValue = "createdAt,desc") String sort) {
    return catalogService.listProducts(page, size, sort);
  }

  @GetMapping("/{productId}")
  public CatalogService.ProductDetails getProduct(@PathVariable long productId) {
    return catalogService.getProduct(productId);
  }
}
