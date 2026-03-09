package com.webpong.study2.app.payment.application;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.auth.domain.AuditEventEntity;
import com.webpong.study2.app.auth.domain.AuditEventRepository;
import com.webpong.study2.app.global.config.FeatureProperties;
import com.webpong.study2.app.global.config.MessagingProperties;
import com.webpong.study2.app.global.error.ConflictException;
import com.webpong.study2.app.global.error.ForbiddenException;
import com.webpong.study2.app.notification.application.NotificationService;
import com.webpong.study2.app.notification.domain.OutboxEventEntity;
import com.webpong.study2.app.notification.domain.OutboxEventRepository;
import com.webpong.study2.app.order.application.OrderService;
import com.webpong.study2.app.order.domain.OrderEntity;
import com.webpong.study2.app.order.domain.OrderStatus;
import com.webpong.study2.app.payment.domain.PaymentEntity;
import com.webpong.study2.app.payment.domain.PaymentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PaymentService {

  private final PaymentRepository paymentRepository;
  private final OrderService orderService;
  private final AuditEventRepository auditEventRepository;
  private final OutboxEventRepository outboxEventRepository;
  private final NotificationService notificationService;
  private final ObjectMapper objectMapper;
  private final FeatureProperties featureProperties;
  private final MessagingProperties messagingProperties;

  public PaymentService(
      PaymentRepository paymentRepository,
      OrderService orderService,
      AuditEventRepository auditEventRepository,
      OutboxEventRepository outboxEventRepository,
      NotificationService notificationService,
      ObjectMapper objectMapper,
      FeatureProperties featureProperties,
      MessagingProperties messagingProperties) {
    this.paymentRepository = paymentRepository;
    this.orderService = orderService;
    this.auditEventRepository = auditEventRepository;
    this.outboxEventRepository = outboxEventRepository;
    this.notificationService = notificationService;
    this.objectMapper = objectMapper;
    this.featureProperties = featureProperties;
    this.messagingProperties = messagingProperties;
  }

  @Transactional
  public PaymentResponse confirmMockPayment(
      String userId, boolean admin, long orderId, String idempotencyKey) {
    PaymentEntity existingPayment =
        paymentRepository.findByIdempotencyKey(idempotencyKey).orElse(null);
    if (existingPayment != null) {
      OrderEntity existingOrder = orderService.requireOrder(existingPayment.getOrderId());
      return PaymentResponse.replayed(existingPayment, existingOrder.getStatus());
    }

    OrderEntity order = orderService.requireOrder(orderId);
    if (!admin && !order.getUserId().equals(userId)) {
      throw new ForbiddenException("Payment access is forbidden");
    }
    if (order.getStatus() == OrderStatus.PAID || order.getStatus() == OrderStatus.FULFILLED) {
      throw new ConflictException("Order is already paid");
    }
    if (order.getStatus() != OrderStatus.PENDING_PAYMENT) {
      throw new ConflictException("Only pending-payment orders can be confirmed");
    }

    PaymentEntity payment =
        paymentRepository.save(
            new PaymentEntity(order.getId(), idempotencyKey, order.getTotalAmount()));
    order.transitionTo(OrderStatus.PAID);
    orderService.confirmReservations(order.getId());
    auditEventRepository.save(
        new AuditEventEntity("order.paid", order.getUserId(), "Order " + order.getId() + " paid"));
    outboxEventRepository.save(
        new OutboxEventEntity(
            "order",
            String.valueOf(order.getId()),
            messagingProperties.orderPaidTopic(),
            serialize(
                new OrderPaidPayload(
                    messagingProperties.orderPaidTopic(),
                    order.getId(),
                    order.getUserId(),
                    order.getTotalAmount()))));
    if (!featureProperties.messagingEnabled()) {
      notificationService.recordOrderPaid(order.getUserId(), order.getId(), order.getTotalAmount());
    }
    return PaymentResponse.confirmed(payment, order.getStatus());
  }

  private String serialize(OrderPaidPayload payload) {
    try {
      return objectMapper.writeValueAsString(payload);
    } catch (JsonProcessingException exception) {
      throw new IllegalStateException("Order-paid payload could not be serialized", exception);
    }
  }

  public record OrderPaidPayload(
      String topic, Long orderId, String userId, java.math.BigDecimal amount) {}

  public record PaymentResponse(
      Long paymentId,
      Long orderId,
      String idempotencyKey,
      com.webpong.study2.app.payment.domain.PaymentStatus paymentStatus,
      OrderStatus orderStatus,
      java.math.BigDecimal amount,
      boolean replayed) {

    static PaymentResponse confirmed(PaymentEntity payment, OrderStatus orderStatus) {
      return new PaymentResponse(
          payment.getId(),
          payment.getOrderId(),
          payment.getIdempotencyKey(),
          payment.getStatus(),
          orderStatus,
          payment.getAmount(),
          false);
    }

    static PaymentResponse replayed(PaymentEntity payment, OrderStatus orderStatus) {
      return new PaymentResponse(
          payment.getId(),
          payment.getOrderId(),
          payment.getIdempotencyKey(),
          payment.getStatus(),
          orderStatus,
          payment.getAmount(),
          true);
    }
  }
}
