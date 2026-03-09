package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
class CommerceApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;

  @Test
  void catalogCartAndOrderFlowWork() throws Exception {
    mockMvc
        .perform(post("/api/v1/auth/login").param("email", "buyer@example.com"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.accessToken").exists());

    MvcResult productResult =
        mockMvc
            .perform(
                post("/api/v1/admin/products")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"name\":\"Monitor\",\"price\":199.99,\"stock\":4}"))
            .andExpect(status().isOk())
            .andReturn();
    JsonNode productJson = objectMapper.readTree(productResult.getResponse().getContentAsString());

    mockMvc
        .perform(get("/api/v1/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].name").value("Monitor"));

    mockMvc
        .perform(
            post("/api/v1/cart/items")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"customerEmail\":\"buyer@example.com\",\"productId\":"
                        + productJson.get("id").asLong()
                        + ",\"quantity\":1}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.itemCount").value(1));

    mockMvc
        .perform(post("/api/v1/orders").param("customerEmail", "buyer@example.com"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("PLACED"));

    mockMvc
        .perform(get("/api/v1/admin/orders"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].customerEmail").value("buyer@example.com"));
  }
}
