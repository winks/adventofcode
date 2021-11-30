package org.f5n.aoc2020;

import java.util.Collections;
import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;


@RestController
public class HelloController {

	@RequestMapping(value = "/", produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<String, String> index() {
		return Collections.singletonMap("message", "Greetings from Spring Boot!");
	}
}
