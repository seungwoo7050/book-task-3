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
class FederationSecurityApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;

  @Test
  void googleCallbackAndAuditFlowWork() throws Exception {
    mockMvc
        .perform(get("/api/v1/auth/google/authorize"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.url").value(org.hamcrest.Matchers.containsString("google")));

    mockMvc
        .perform(
            post("/api/v1/auth/google/callback")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"oauth@example.com\",\"subject\":\"google-123\"}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.provider").value("google"));

    mockMvc
        .perform(get("/api/v1/audit-events"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].type").exists());
  }

  @Test
  void totpSetupAndVerifyFlowWork() throws Exception {
    MvcResult setup =
        mockMvc
            .perform(
                post("/api/v1/auth/2fa/setup")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"email\":\"totp@example.com\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.recoveryCodes[0]").exists())
            .andReturn();

    JsonNode setupJson = objectMapper.readTree(setup.getResponse().getContentAsString());
    String expectedCode = setupJson.get("expectedCode").asText();

    mockMvc
        .perform(
            post("/api/v1/auth/2fa/verify")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"totp@example.com\",\"code\":\"" + expectedCode + "\"}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.verified").value(true));
  }
}
