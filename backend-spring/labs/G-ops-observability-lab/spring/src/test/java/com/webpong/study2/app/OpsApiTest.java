package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class OpsApiTest {

  @Autowired private MockMvc mockMvc;

  @Test
  void summaryExposesOperationalLinks() throws Exception {
    mockMvc
        .perform(get("/api/v1/ops/summary"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.metrics").value("/actuator/prometheus"))
        .andExpect(jsonPath("$.health").value("/api/v1/health/ready"));
  }
}
