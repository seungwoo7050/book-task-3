package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class CacheConcurrencyApiTest {

  @Autowired private MockMvc mockMvc;

  @Test
  void idempotentReservationReturnsSameResult() throws Exception {
    mockMvc
        .perform(
            post("/api/v1/inventory/reservations")
                .header("Idempotency-Key", "reserve-1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"sku\":\"SKU-1\",\"quantity\":2}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.remaining").value(8));

    mockMvc
        .perform(
            post("/api/v1/inventory/reservations")
                .header("Idempotency-Key", "reserve-1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"sku\":\"SKU-1\",\"quantity\":2}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.remaining").value(8));

    mockMvc
        .perform(get("/api/v1/inventory/SKU-1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.available").value(8));
  }
}
