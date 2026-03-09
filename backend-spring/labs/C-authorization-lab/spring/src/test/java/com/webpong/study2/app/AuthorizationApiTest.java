package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
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
class AuthorizationApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;

  @Test
  void inviteAcceptAndRoleChangeFlowWork() throws Exception {
    MvcResult organizationResult =
        mockMvc
            .perform(
                post("/api/v1/organizations")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"name\":\"Store Ops\",\"ownerEmail\":\"owner@example.com\"}"))
            .andExpect(status().isOk())
            .andReturn();
    long organizationId =
        objectMapper
            .readTree(organizationResult.getResponse().getContentAsString())
            .get("id")
            .asLong();

    MvcResult inviteResult =
        mockMvc
            .perform(
                post("/api/v1/organizations/{organizationId}/invites", organizationId)
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"email\":\"staff@example.com\",\"role\":\"STAFF\"}"))
            .andExpect(status().isOk())
            .andReturn();
    JsonNode inviteJson = objectMapper.readTree(inviteResult.getResponse().getContentAsString());

    mockMvc
        .perform(post("/api/v1/invitations/{invitationId}/accept", inviteJson.get("id").asLong()))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.role").value("STAFF"));

    mockMvc
        .perform(
            patch(
                    "/api/v1/organizations/{organizationId}/members/{email}/role",
                    organizationId,
                    "staff@example.com")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"role\":\"MANAGER\"}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.role").value("MANAGER"));
  }
}
