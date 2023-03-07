package com.divanv.muninn;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.divanv.muninn.chats.TelegramBotImpl;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

import com.divanv.muninn.actors.core.GuardianActor;
import org.springframework.context.annotation.Scope;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

import static com.divanv.muninn.SpringExtension.SPRING_EXTENSION_PROVIDER;

@Configuration
@ComponentScan
@EnableJpaAuditing
public class AppConfiguration {

    @Autowired
    private ApplicationContext applicationContext;

    @Bean
    public ActorSystem actorSystem() {
        var system = ActorSystem.create("MuninnActorSystem");
        SPRING_EXTENSION_PROVIDER.get(system)
                .initialize(applicationContext);
        return system;
    }

    @Bean
    public ActorRef smartSwitchActor(@Autowired ActorSystem actorSystem) {
        return actorSystem.actorOf(Props.create(GuardianActor.class));
    }

    @Bean
    @Scope("singleton")
    TelegramBotImpl telegramBotImpl() {
        return new TelegramBotImpl();
    }

    @Bean
    public DataSource dataSource() {
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl("jdbc:postgresql://localhost:5432/muninn");
        dataSource.setUsername("user");
        dataSource.setPassword("pass");
        // set other properties here
        return dataSource;
    }
}
