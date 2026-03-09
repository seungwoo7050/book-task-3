package com.webpong.study2.app;

import com.webpong.study2.app.global.config.AppProperties;
import com.webpong.study2.app.global.config.AuthProperties;
import com.webpong.study2.app.global.config.BootstrapAdminProperties;
import com.webpong.study2.app.global.config.FeatureProperties;
import com.webpong.study2.app.global.config.MessagingProperties;
import com.webpong.study2.app.global.config.RateLimitProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
@EnableCaching
@EnableKafka
@EnableConfigurationProperties({
  AppProperties.class,
  AuthProperties.class,
  BootstrapAdminProperties.class,
  FeatureProperties.class,
  MessagingProperties.class,
  RateLimitProperties.class
})
public class Study2Application {

  public static void main(String[] args) {
    SpringApplication.run(Study2Application.class, args);
  }
}
