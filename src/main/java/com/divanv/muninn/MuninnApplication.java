package com.divanv.muninn;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.divanv.muninn.actors.SmartSwitchActor;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

@SpringBootApplication
public class MuninnApplication {

	private static Logger logger = LoggerFactory.getLogger(MuninnApplication.class);

	public static void main(String[] args) {
		SpringApplication.run(MuninnApplication.class, args);

		// Start the akka system
		var system = ActorSystem.create("Muninn");
		var myActor = system.actorOf(Props.create(SmartSwitchActor.class));

		ApplicationContext context = new AnnotationConfigApplicationContext(AkkaConfiguration.class);
		// Telegram bot
		var bot = context.getBean(TelegramBotImpl.class);

		// start the bot
		try {
			TelegramBotsApi telegramBotsApi = new TelegramBotsApi(DefaultBotSession.class);
			telegramBotsApi.registerBot(bot);
		} catch (TelegramApiException e) {
			logger.error("Telegram bot registration failed",e);
			throw new RuntimeException(e);
		}
		var chatId = "70661797";
		SendMessage message = new SendMessage();
		message.setChatId(chatId);
		message.setText("I awaken once again.");

		try {
			bot.execute(message);
		} catch (TelegramApiException e) {
			throw new RuntimeException(e);
		}
	}

}
