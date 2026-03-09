package com.webpong.study2.app.global.api;

import java.time.Instant;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/health")
public class HealthController {

  @GetMapping("/live")
  public Map<String, Object> live() {
    return Map.of("status", "UP", "kind", "live", "checkedAt", Instant.now().toString());
  }

  @GetMapping("/ready")
  public Map<String, Object> ready() {
    return Map.of("status", "UP", "kind", "ready", "checkedAt", Instant.now().toString());
  }
}
