package com.webpong.study2.app.commerce.api;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class CommerceAuthController {

  @PostMapping("/auth/login")
  public Map<String, String> login(@RequestParam String email) {
    return Map.of("accessToken", "commerce-access-token", "email", email);
  }

  @GetMapping("/me")
  public Map<String, String> me(@RequestParam String email) {
    return Map.of("email", email, "role", "CUSTOMER");
  }
}
