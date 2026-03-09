package com.webpong.study2.app.events.api;

import com.webpong.study2.app.events.application.EventMessagingService;
import jakarta.validation.constraints.NotBlank;
import java.util.List;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/v1")
public class EventMessagingController {

  private final EventMessagingService service;

  public EventMessagingController(EventMessagingService service) {
    this.service = service;
  }

  @PostMapping("/orders/{orderId}/events")
  public EventMessagingService.EventResponse emit(@PathVariable @NotBlank String orderId) {
    return service.emitOrderPlaced(orderId);
  }

  @PostMapping("/outbox-events/publish")
  public List<EventMessagingService.EventResponse> publish() {
    return service.publishPending();
  }

  @GetMapping("/outbox-events")
  public List<EventMessagingService.EventResponse> list() {
    return service.list();
  }
}
