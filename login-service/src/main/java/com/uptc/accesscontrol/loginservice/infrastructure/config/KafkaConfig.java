package com.uptc.accesscontrol.loginservice.infrastructure.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

@Configuration
public class KafkaConfig {

    @Bean
    public NewTopic alertNotificationTopic() {
        return TopicBuilder.name("alert-notification")
                .partitions(3)
                .replicas(1)
                .build();
    }
}
