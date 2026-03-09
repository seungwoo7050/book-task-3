package com.webpong.study2.app.payment.api;

import com.webpong.study2.app.global.security.AuthenticationFacade;
import com.webpong.study2.app.payment.application.PaymentService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/payments/mock")
public class PaymentController {

  private final PaymentService paymentService;
  private final AuthenticationFacade authenticationFacade;

  public PaymentController(
      PaymentService paymentService, AuthenticationFacade authenticationFacade) {
    this.paymentService = paymentService;
    this.authenticationFacade = authenticationFacade;
  }

  @PostMapping("/confirm")
  public PaymentService.PaymentResponse confirm(
      @RequestHeader("Idempotency-Key") String idempotencyKey,
      @Valid @RequestBody PaymentConfirmRequest request) {
    return paymentService.confirmMockPayment(
        authenticationFacade.currentUser().userId(),
        authenticationFacade.currentUser().hasRole("ADMIN"),
        request.orderId(),
        idempotencyKey);
  }

  public record PaymentConfirmRequest(@NotNull Long orderId) {}
}
