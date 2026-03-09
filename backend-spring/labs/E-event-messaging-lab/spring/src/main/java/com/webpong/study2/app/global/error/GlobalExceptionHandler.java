package com.webpong.study2.app.global.error;

import java.net.URI;
import java.util.List;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(IllegalArgumentException.class)
  ProblemDetail handleIllegalArgument(IllegalArgumentException exception) {
    return createProblem(HttpStatus.BAD_REQUEST, "bad_request", exception.getMessage(), List.of());
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  ProblemDetail handleValidation(MethodArgumentNotValidException exception) {
    List<String> errors =
        exception.getBindingResult().getFieldErrors().stream()
            .map(error -> error.getField() + ": " + error.getDefaultMessage())
            .toList();
    return createProblem(HttpStatus.BAD_REQUEST, "validation_failed", "Validation failed", errors);
  }

  private ProblemDetail createProblem(
      HttpStatus status, String code, String detail, List<String> errors) {
    ProblemDetail problemDetail = ProblemDetail.forStatusAndDetail(status, detail);
    problemDetail.setTitle(status.getReasonPhrase());
    problemDetail.setType(URI.create("https://example.local/problems/" + code));
    problemDetail.setProperty("code", code);
    problemDetail.setProperty("traceId", MDC.get("traceId"));
    problemDetail.setProperty("errors", errors);
    return problemDetail;
  }
}
