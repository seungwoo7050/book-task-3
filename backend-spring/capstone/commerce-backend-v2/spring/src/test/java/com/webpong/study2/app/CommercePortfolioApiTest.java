package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webpong.study2.app.notification.domain.NotificationRepository;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
class CommercePortfolioApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;
  @Autowired private NotificationRepository notificationRepository;

  @Test
  void adminCatalogCustomerCheckoutAndPaymentFlowWorks() throws Exception {
    String adminAccessToken = login("admin@study2.local", "Admin1234!").accessToken();
    String customerEmail = "customer-" + UUID.randomUUID() + "@example.com";

    mockMvc
        .perform(
            post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {
                      "email": "%s",
                      "password": "Password123!",
                      "displayName": "Customer"
                    }
                    """
                        .formatted(customerEmail)))
        .andExpect(status().isCreated());

    String customerAccessToken = login(customerEmail, "Password123!").accessToken();

    MvcResult categoryResult =
        mockMvc
            .perform(
                post("/api/v1/admin/categories")
                    .header("Authorization", "Bearer " + adminAccessToken)
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(
                        """
                        {
                          "name": "Displays",
                          "slug": "displays-%s"
                        }
                        """
                            .formatted(UUID.randomUUID())))
            .andExpect(status().isCreated())
            .andReturn();
    long categoryId =
        objectMapper.readTree(categoryResult.getResponse().getContentAsString()).get("id").asLong();

    MvcResult productResult =
        mockMvc
            .perform(
                post("/api/v1/admin/products")
                    .header("Authorization", "Bearer " + adminAccessToken)
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(
                        """
                        {
                          "categoryId": %d,
                          "name": "Monitor Pro",
                          "description": "A portfolio-grade test product",
                          "price": 199.99,
                          "stock": 3
                        }
                        """
                            .formatted(categoryId)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("Monitor Pro"))
            .andReturn();
    long productId =
        objectMapper.readTree(productResult.getResponse().getContentAsString()).get("id").asLong();

    mockMvc
        .perform(get("/api/v1/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content[0].name").value("Monitor Pro"));

    mockMvc
        .perform(
            post("/api/v1/cart/items")
                .header("Authorization", "Bearer " + customerAccessToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {
                      "productId": %d,
                      "quantity": 1
                    }
                    """
                        .formatted(productId)))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.itemCount").value(1))
        .andExpect(jsonPath("$.totalAmount").value(199.99));

    MvcResult orderResult =
        mockMvc
            .perform(
                post("/api/v1/orders").header("Authorization", "Bearer " + customerAccessToken))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("PENDING_PAYMENT"))
            .andReturn();
    long orderId =
        objectMapper
            .readTree(orderResult.getResponse().getContentAsString())
            .get("orderId")
            .asLong();

    mockMvc
        .perform(
            post("/api/v1/payments/mock/confirm")
                .header("Authorization", "Bearer " + customerAccessToken)
                .header("Idempotency-Key", "idem-" + orderId)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"orderId\": %d}".formatted(orderId)))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.orderStatus").value("PAID"))
        .andExpect(jsonPath("$.replayed").value(false));

    mockMvc
        .perform(
            post("/api/v1/payments/mock/confirm")
                .header("Authorization", "Bearer " + customerAccessToken)
                .header("Idempotency-Key", "idem-" + orderId)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"orderId\": %d}".formatted(orderId)))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.orderStatus").value("PAID"))
        .andExpect(jsonPath("$.replayed").value(true));

    mockMvc
        .perform(
            get("/api/v1/orders/{orderId}", orderId)
                .header("Authorization", "Bearer " + customerAccessToken))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("PAID"))
        .andExpect(jsonPath("$.items[0].productName").value("Monitor Pro"));

    mockMvc
        .perform(
            patch("/api/v1/admin/orders/{orderId}/status", orderId)
                .header("Authorization", "Bearer " + adminAccessToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"status\": \"FULFILLED\"}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("FULFILLED"));

    mockMvc
        .perform(get("/api/v1/admin/orders").header("Authorization", "Bearer " + adminAccessToken))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content[0].orderId").value(orderId));

    org.assertj.core.api.Assertions.assertThat(
            notificationRepository.findByDedupKey("order-paid:" + orderId))
        .isPresent();
  }

  private Session login(String email, String password) throws Exception {
    MvcResult loginResult =
        mockMvc
            .perform(
                post("/api/v1/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
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
    JsonNode json = objectMapper.readTree(loginResult.getResponse().getContentAsString());
    return new Session(json.get("accessToken").asText());
  }

  private record Session(String accessToken) {}
}
