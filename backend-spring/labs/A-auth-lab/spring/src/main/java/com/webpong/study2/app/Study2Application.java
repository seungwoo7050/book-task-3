package com.webpong.study2.app;

import com.webpong.study2.app.global.config.AppProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableConfigurationProperties(AppProperties.class)
@EnableCaching
public class Study2Application {

  public static void main(String[] args) {
    SpringApplication.run(Study2Application.class, args);
  }
}
