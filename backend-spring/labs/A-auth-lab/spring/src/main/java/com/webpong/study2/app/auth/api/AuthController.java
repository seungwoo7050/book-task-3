package com.webpong.study2.app.auth.api;

import com.webpong.study2.app.auth.application.AuthDemoService;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

  private final AuthDemoService authDemoService;

  public AuthController(AuthDemoService authDemoService) {
    this.authDemoService = authDemoService;
  }

  @PostMapping("/register")
  @ResponseStatus(HttpStatus.CREATED)
  public AuthDemoService.RegisterResult register(@RequestBody RegisterRequest request) {
    return authDemoService.register(request.email(), request.password());
  }

  @PostMapping("/login")
  public AuthDemoService.SessionSnapshot login(@RequestBody LoginRequest request) {
    return authDemoService.login(request.email(), request.password());
  }

  @PostMapping("/refresh")
  public AuthDemoService.SessionSnapshot refresh(
      @RequestHeader("X-CSRF-TOKEN") String csrfToken, @RequestBody RefreshRequest request) {
    return authDemoService.refresh(request.refreshToken(), csrfToken);
  }

  @PostMapping("/logout")
  public Map<String, String> logout(
      @RequestHeader("X-CSRF-TOKEN") String csrfToken, @RequestBody RefreshRequest request) {
    authDemoService.logout(request.refreshToken(), csrfToken);
    return Map.of("status", "logged_out");
  }

  @GetMapping("/me")
  public AuthDemoService.UserProfile me(@RequestParam @Email String email) {
    return authDemoService.me(email);
  }

  public record RegisterRequest(@Email String email, @NotBlank String password) {}

  public record LoginRequest(@Email String email, @NotBlank String password) {}

  public record RefreshRequest(@NotBlank String refreshToken) {}
}
