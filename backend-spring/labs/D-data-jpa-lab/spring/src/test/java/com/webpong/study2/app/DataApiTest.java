package com.webpong.study2.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
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
class DataApiTest {

  @Autowired private MockMvc mockMvc;
  @Autowired private ObjectMapper objectMapper;

  @Test
  void productCrudAndConflictCheckWork() throws Exception {
    MvcResult created =
        mockMvc
            .perform(
                post("/api/v1/products")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"name\":\"Keyboard\",\"price\":129.99}"))
            .andExpect(status().isOk())
            .andReturn();

    JsonNode product = objectMapper.readTree(created.getResponse().getContentAsString());

    mockMvc
        .perform(get("/api/v1/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content[0].name").value("Keyboard"));

    mockMvc
        .perform(
            patch("/api/v1/products/{productId}", product.get("id").asLong())
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"price\":149.99,\"version\":0}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.price").value(149.99));

    mockMvc
        .perform(
            patch("/api/v1/products/{productId}", product.get("id").asLong())
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"price\":159.99,\"version\":0}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("bad_request"));
  }
}
