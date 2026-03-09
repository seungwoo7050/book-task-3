package com.webpong.study2.app.auth.api;

import com.webpong.study2.app.auth.application.AuthService;
import com.webpong.study2.app.global.security.AuthenticationFacade;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1")
public class AuthController {

  private final AuthService authService;
  private final AuthenticationFacade authenticationFacade;

  public AuthController(AuthService authService, AuthenticationFacade authenticationFacade) {
    this.authService = authService;
    this.authenticationFacade = authenticationFacade;
  }

  @PostMapping("/auth/register")
  @ResponseStatus(HttpStatus.CREATED)
  public AuthService.AuthUserProfile register(@Valid @RequestBody RegisterRequest request) {
    return authService.register(request.email(), request.password(), request.displayName());
  }

  @PostMapping("/auth/login")
  public SessionResponse login(
      @Valid @RequestBody LoginRequest request, HttpServletResponse response) {
    AuthService.SessionSnapshot session = authService.login(request.email(), request.password());
    writeSessionCookies(response, session.refreshToken(), session.csrfToken(), false);
    return new SessionResponse(session.accessToken(), session.csrfToken(), session.user());
  }

  @GetMapping("/auth/google/authorize")
  public AuthService.AuthorizationUrl authorize() {
    return authService.issueGoogleAuthorizationUrl();
  }

  @PostMapping("/auth/google/callback")
  public SessionResponse googleCallback(
      @Valid @RequestBody GoogleCallbackRequest request, HttpServletResponse response) {
    AuthService.SessionSnapshot session =
        authService.googleCallback(
            request.state(),
            request.nonce(),
            request.email(),
            request.subject(),
            request.displayName());
    writeSessionCookies(response, session.refreshToken(), session.csrfToken(), false);
    return new SessionResponse(session.accessToken(), session.csrfToken(), session.user());
  }

  @PostMapping("/auth/refresh")
  public SessionResponse refresh(
      @CookieValue("refresh_token") String refreshToken,
      @RequestHeader("X-CSRF-TOKEN") String csrfToken,
      HttpServletResponse response) {
    AuthService.SessionSnapshot session = authService.refresh(refreshToken, csrfToken);
    writeSessionCookies(response, session.refreshToken(), session.csrfToken(), false);
    return new SessionResponse(session.accessToken(), session.csrfToken(), session.user());
  }

  @PostMapping("/auth/logout")
  public LogoutResponse logout(
      @CookieValue("refresh_token") String refreshToken,
      @RequestHeader("X-CSRF-TOKEN") String csrfToken,
      HttpServletResponse response) {
    authService.logout(refreshToken, csrfToken);
    writeSessionCookies(response, "", "", true);
    return new LogoutResponse("logged_out");
  }

  @GetMapping("/me")
  public AuthService.AuthUserProfile me() {
    return authService.me(authenticationFacade.currentUser().userId());
  }

  private void writeSessionCookies(
      HttpServletResponse response, String refreshToken, String csrfToken, boolean clear) {
    ResponseCookie refreshCookie =
        ResponseCookie.from("refresh_token", refreshToken)
            .httpOnly(true)
            .sameSite("Lax")
            .path("/api/v1/auth")
            .maxAge(clear ? 0 : 60L * 60L * 24L * 14L)
            .build();
    ResponseCookie csrfCookie =
        ResponseCookie.from("XSRF-TOKEN", csrfToken)
            .httpOnly(false)
            .sameSite("Lax")
            .path("/")
            .maxAge(clear ? 0 : 60L * 60L * 24L * 14L)
            .build();
    response.addHeader(HttpHeaders.SET_COOKIE, refreshCookie.toString());
    response.addHeader(HttpHeaders.SET_COOKIE, csrfCookie.toString());
  }

  public record RegisterRequest(
      @Email String email, @NotBlank String password, @NotBlank String displayName) {}

  public record LoginRequest(@Email String email, @NotBlank String password) {}

  public record GoogleCallbackRequest(
      @NotBlank String state,
      @NotBlank String nonce,
      @Email String email,
      @NotBlank String subject,
      @NotBlank String displayName) {}

  public record SessionResponse(
      String accessToken, String csrfToken, AuthService.AuthUserProfile user) {}

  public record LogoutResponse(String status) {}
}
