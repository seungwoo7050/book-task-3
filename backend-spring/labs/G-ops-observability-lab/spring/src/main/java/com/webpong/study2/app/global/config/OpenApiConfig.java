package com.webpong.study2.app.global.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

  @Bean
  OpenAPI study2OpenApi(AppProperties appProperties) {
    return new OpenAPI()
        .info(
            new Info()
                .title(appProperties.name() + " API")
                .version("v1")
                .description(appProperties.summary()));
  }
}
