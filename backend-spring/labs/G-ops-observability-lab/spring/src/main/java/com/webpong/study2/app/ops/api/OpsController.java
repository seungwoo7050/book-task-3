package com.webpong.study2.app.ops.api;

import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/ops")
public class OpsController {

  @Value("${spring.profiles.active:local}")
  private String activeProfile;

  @GetMapping("/summary")
  public Map<String, Object> summary() {
    return Map.of(
        "profile", activeProfile,
        "metrics", "/actuator/prometheus",
        "docs", "/swagger-ui.html",
        "health", "/api/v1/health/ready");
  }
}
