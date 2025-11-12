package com.uptc.alertservice.infrastructure.kafka;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

@Configuration
public class KafkaConfig {
    
    @Value("${kafka.topic.alert-notification}")
    private String alertNotificationTopic;
    
    @Bean
    public NewTopic alertNotificationTopic() {
        return TopicBuilder.name(alertNotificationTopic)
                .partitions(3)
                .replicas(1)
                .build();
    }
}
