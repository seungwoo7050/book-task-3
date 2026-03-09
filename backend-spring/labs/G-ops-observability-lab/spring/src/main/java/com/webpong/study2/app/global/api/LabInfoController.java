package com.webpong.study2.app.global.api;

import com.webpong.study2.app.global.config.AppProperties;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/lab")
public class LabInfoController {

  private final AppProperties appProperties;

  public LabInfoController(AppProperties appProperties) {
    this.appProperties = appProperties;
  }

  @GetMapping("/info")
  public Map<String, Object> info() {
    return Map.of(
        "name", appProperties.name(),
        "track", appProperties.track(),
        "summary", appProperties.summary());
  }
}
