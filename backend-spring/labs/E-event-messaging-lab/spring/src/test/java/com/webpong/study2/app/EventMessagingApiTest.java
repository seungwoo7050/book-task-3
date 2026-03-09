package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class EventMessagingApiTest {

  @Autowired private MockMvc mockMvc;

  @Test
  void outboxEventLifecycleWorks() throws Exception {
    mockMvc
        .perform(post("/api/v1/orders/{orderId}/events", "ORDER-1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("PENDING"));

    mockMvc
        .perform(post("/api/v1/outbox-events/publish"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].status").value("PUBLISHED"));

    mockMvc
        .perform(get("/api/v1/outbox-events"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].eventType").value("ORDER_PLACED"));
  }
}
