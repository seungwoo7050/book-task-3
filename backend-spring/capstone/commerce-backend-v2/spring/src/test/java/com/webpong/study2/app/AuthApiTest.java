package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.Cookie;
import java.util.List;
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
class AuthApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;

  @Test
  void registerLoginRefreshLogoutFlowWorks() throws Exception {
    String email = "buyer-" + UUID.randomUUID() + "@example.com";

    mockMvc
        .perform(
            post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {
                      "email": "%s",
                      "password": "Password123!",
                      "displayName": "Buyer"
                    }
                    """
                        .formatted(email)))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.email").value(email))
        .andExpect(jsonPath("$.roles[0]").value("CUSTOMER"));

    Session loginSession = login(email, "Password123!");

    mockMvc
        .perform(get("/api/v1/me").header("Authorization", "Bearer " + loginSession.accessToken()))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.email").value(email))
        .andExpect(jsonPath("$.displayName").value("Buyer"));

    mockMvc
        .perform(
            post("/api/v1/auth/refresh")
                .cookie(new Cookie("refresh_token", loginSession.refreshToken()))
                .header("X-CSRF-TOKEN", "wrong-token"))
        .andExpect(status().isUnauthorized());

    MvcResult refreshResult =
        mockMvc
            .perform(
                post("/api/v1/auth/refresh")
                    .cookie(new Cookie("refresh_token", loginSession.refreshToken()))
                    .header("X-CSRF-TOKEN", loginSession.csrfToken()))
            .andExpect(status().isOk())
            .andReturn();
    org.assertj.core.api.Assertions.assertThat(refreshResult.getResponse().getHeaders("Set-Cookie"))
        .hasSize(2);

    Session refreshedSession = toSession(refreshResult);

    mockMvc
        .perform(
            post("/api/v1/auth/logout")
                .cookie(new Cookie("refresh_token", refreshedSession.refreshToken()))
                .header("X-CSRF-TOKEN", refreshedSession.csrfToken()))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("logged_out"));

    mockMvc
        .perform(
            post("/api/v1/auth/refresh")
                .cookie(new Cookie("refresh_token", refreshedSession.refreshToken()))
                .header("X-CSRF-TOKEN", refreshedSession.csrfToken()))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void googleCallbackLinksExistingLocalAccount() throws Exception {
    String email = "google-link-" + UUID.randomUUID() + "@example.com";
    mockMvc
        .perform(
            post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {
                      "email": "%s",
                      "password": "Password123!",
                      "displayName": "Linked User"
                    }
                    """
                        .formatted(email)))
        .andExpect(status().isCreated());

    MvcResult authorizeResult =
        mockMvc
            .perform(get("/api/v1/auth/google/authorize"))
            .andExpect(status().isOk())
            .andReturn();
    JsonNode authorizeJson =
        objectMapper.readTree(authorizeResult.getResponse().getContentAsString());

    MvcResult callbackResult =
        mockMvc
            .perform(
                post("/api/v1/auth/google/callback")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(
                        """
                        {
                          "state": "%s",
                          "nonce": "%s",
                          "email": "%s",
                          "subject": "google-%s",
                          "displayName": "Linked User"
                        }
                        """
                            .formatted(
                                authorizeJson.get("state").asText(),
                                authorizeJson.get("nonce").asText(),
                                email,
                                UUID.randomUUID())))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.user.email").value(email))
            .andReturn();

    Session callbackSession = toSession(callbackResult);
    mockMvc
        .perform(
            get("/api/v1/me").header("Authorization", "Bearer " + callbackSession.accessToken()))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.email").value(email));
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
    return toSession(loginResult);
  }

  private Session toSession(MvcResult result) throws Exception {
    JsonNode json = objectMapper.readTree(result.getResponse().getContentAsString());
    List<String> setCookieHeaders = result.getResponse().getHeaders("Set-Cookie");
    return new Session(
        json.get("accessToken").asText(),
        extractCookieValue(setCookieHeaders, "refresh_token"),
        json.get("csrfToken").asText());
  }

  private String extractCookieValue(List<String> headers, String cookieName) {
    return headers.stream()
        .filter(header -> header.startsWith(cookieName + "="))
        .findFirst()
        .map(
            header -> {
              int end = header.indexOf(';');
              return end >= 0
                  ? header.substring(cookieName.length() + 1, end)
                  : header.substring(cookieName.length() + 1);
            })
        .orElseThrow();
  }

  private record Session(String accessToken, String refreshToken, String csrfToken) {}
}
