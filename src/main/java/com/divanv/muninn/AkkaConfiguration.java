package com.divanv.muninn;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.divanv.muninn.actors.core.GuardianActor;
import org.springframework.context.annotation.Scope;

@Configuration
public class AkkaConfiguration {
    @Bean
    public ActorSystem actorSystem() {
        return ActorSystem.create("MuninnActorSystem");
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
}
