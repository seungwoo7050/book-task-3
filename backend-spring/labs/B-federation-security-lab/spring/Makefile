run:
	SPRING_PROFILES_ACTIVE=local ./gradlew bootRun

lint:
	./gradlew spotlessCheck checkstyleMain checkstyleTest

test:
	./gradlew test

smoke:
	./gradlew test --tests '*SmokeTest'
