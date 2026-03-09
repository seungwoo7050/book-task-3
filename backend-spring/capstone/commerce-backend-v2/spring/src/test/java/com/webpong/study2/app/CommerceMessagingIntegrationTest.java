package com.webpong.study2.app;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.notification.domain.NotificationRepository;
import com.webpong.study2.app.notification.infrastructure.OutboxPublisher;
import java.time.Duration;
import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.KafkaContainer;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class CommerceMessagingIntegrationTest {

  @Container
  static PostgreSQLContainer<?> postgres =
      new PostgreSQLContainer<>(DockerImageName.parse("postgres:16-alpine"));

  @Container
  static GenericContainer<?> redis =
      new GenericContainer<>(DockerImageName.parse("redis:7-alpine")).withExposedPorts(6379);

  @Container
  static KafkaContainer kafka =
      new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.6.1"));

  @DynamicPropertySource
  static void registerProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
    registry.add("spring.datasource.driver-class-name", () -> "org.postgresql.Driver");
    registry.add("spring.data.redis.host", redis::getHost);
    registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
    registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    registry.add("app.features.redis-cart-enabled", () -> true);
    registry.add("app.features.redis-rate-limit-enabled", () -> true);
    registry.add("app.features.messaging-enabled", () -> true);
    registry.add("app.messaging.publish-delay-ms", () -> 100L);
  }

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;
  @Autowired private OutboxPublisher outboxPublisher;
  @Autowired private NotificationRepository notificationRepository;

  @Test
  void orderPaidEventIsPublishedAndConsumed() throws Exception {
    String adminToken = login("admin@study2.local", "Admin1234!").asText();
    String customerEmail = "integration-" + UUID.randomUUID() + "@example.com";
    mockMvc
        .perform(
            post("/api/v1/auth/register")
                .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                .content(
                    """
                    {
                      "email": "%s",
                      "password": "Password123!",
                      "displayName": "Integration User"
                    }
                    """
                        .formatted(customerEmail)))
        .andExpect(status().isCreated());
    String customerToken = login(customerEmail, "Password123!").asText();

    long categoryId =
        json(mockMvc
                .perform(
                    post("/api/v1/admin/categories")
                        .header("Authorization", "Bearer " + adminToken)
                        .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                        .content(
                            "{\"name\":\"Integration\",\"slug\":\"integration-"
                                + UUID.randomUUID()
                                + "\"}"))
                .andExpect(status().isCreated())
                .andReturn())
            .get("id")
            .asLong();
    long productId =
        json(mockMvc
                .perform(
                    post("/api/v1/admin/products")
                        .header("Authorization", "Bearer " + adminToken)
                        .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                        .content(
                            """
                                {
                                  "categoryId": %d,
                                  "name": "Event Product",
                                  "description": "Triggers Kafka",
                                  "price": 29.99,
                                  "stock": 5
                                }
                                """
                                .formatted(categoryId)))
                .andExpect(status().isCreated())
                .andReturn())
            .get("id")
            .asLong();

    mockMvc
        .perform(
            post("/api/v1/cart/items")
                .header("Authorization", "Bearer " + customerToken)
                .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                .content("{\"productId\": %d, \"quantity\": 1}".formatted(productId)))
        .andExpect(status().isOk());

    long orderId =
        json(mockMvc
                .perform(post("/api/v1/orders").header("Authorization", "Bearer " + customerToken))
                .andExpect(status().isOk())
                .andReturn())
            .get("orderId")
            .asLong();

    mockMvc
        .perform(
            post("/api/v1/payments/mock/confirm")
                .header("Authorization", "Bearer " + customerToken)
                .header("Idempotency-Key", "kafka-" + orderId)
                .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                .content("{\"orderId\": %d}".formatted(orderId)))
        .andExpect(status().isOk());

    outboxPublisher.publishPending();

    Instant deadline = Instant.now().plus(Duration.ofSeconds(10));
    while (Instant.now().isBefore(deadline)
        && notificationRepository.findByDedupKey("order-paid:" + orderId).isEmpty()) {
      Thread.sleep(200L);
    }

    assertThat(notificationRepository.findByDedupKey("order-paid:" + orderId)).isPresent();
  }

  private JsonNode login(String email, String password) throws Exception {
    MvcResult result =
        mockMvc
            .perform(
                post("/api/v1/auth/login")
                    .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                    .content(
                        """
                        {
                          "email": "%s",
                          "password": "%s"
                        }
                        """
                            .formatted(email, password)))
            .andExpect(status().isOk())
            .andReturn();
    return json(result).get("accessToken");
  }

  private JsonNode json(MvcResult result) throws Exception {
    return objectMapper.readTree(result.getResponse().getContentAsString());
  }
}
