package org.f5n.aoc2020;

import java.util.Arrays;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class Aoc2020Application {

	public static void main(String[] args) {
		SpringApplication.run(Aoc2020Application.class, args);
	}

	@Bean
	public CommandLineRunner commandLineRunner(ApplicationContext ctx) {
		return args -> {};
			//System.out.println("beans:");
			//String[] beanNames = ctx.getBeanDefinitionNames();
			//Arrays.sort(beanNames);
			//for (String bean: beanNames) {
			//	System.out.println(bean);
			//}
	}

}
