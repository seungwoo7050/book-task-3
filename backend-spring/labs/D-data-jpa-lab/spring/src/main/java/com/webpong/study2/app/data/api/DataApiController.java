package com.webpong.study2.app.data.api;

import com.webpong.study2.app.data.application.DataApiService;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.math.BigDecimal;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1/products")
public class DataApiController {

  private final DataApiService service;

  public DataApiController(DataApiService service) {
    this.service = service;
  }

  @PostMapping
  public DataApiService.ProductResponse create(@RequestBody CreateRequest request) {
    return service.create(request.name(), request.price());
  }

  @GetMapping
  public DataApiService.PageEnvelope<DataApiService.ProductResponse> list(
      @RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "20") int size) {
    return service.list(page, size);
  }

  @PatchMapping("/{productId}")
  public DataApiService.ProductResponse update(
      @PathVariable long productId, @RequestBody UpdateRequest request) {
    return service.updatePrice(productId, request.version(), request.price());
  }

  public record CreateRequest(@NotBlank String name, @Min(0) BigDecimal price) {}

  public record UpdateRequest(@Min(0) BigDecimal price, long version) {}
}
