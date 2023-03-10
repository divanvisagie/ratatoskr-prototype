package com.divanv.muninn;

import akka.actor.ActorSystem;
import akka.actor.Props;
import com.divanv.muninn.actors.core.GuardianActor;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

import static com.divanv.muninn.SpringExtension.SPRING_EXTENSION_PROVIDER;

@SpringBootApplication
public class MuninnApplication {

	private static Logger logger = LoggerFactory.getLogger(MuninnApplication.class);

	public static void main(String[] args) {
		SpringApplication.run(MuninnApplication.class, args);

		ApplicationContext context = new AnnotationConfigApplicationContext(AppConfiguration.class);
		// Start the akka system
		//var system = ActorSystem.create("Muninn");
		//var myActor = system.actorOf(Props.create(GuardianActor.class));

//		var system = context.getBean(ActorSystem.class);
//		var guardianActorRef = system.actorOf(SPRING_EXTENSION_PROVIDER.get(system)
//						.props("guardianActor"), "guardianActor");




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
