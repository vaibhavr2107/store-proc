## PaymentService

- Domain: payment
- Owned Tables: payments, payment_methods
- Dependencies: None
- Summary: PaymentService coordinates payment domain responsibilities across tables payments, payment_methods.

### Overview
PaymentService coordinates payment domain responsibilities across tables payments, payment_methods.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/paymentservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/controller/PaymentController.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/entity/PaymentEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/mapper/PaymentMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/repository/PaymentRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/service/impl/PaymentServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentservice/service/PaymentService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- api/target/classes/application.yml: Spring Boot application settings.
- api/target/classes/com/barclays/uscb/paymentservice/Application.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/controller/PaymentController.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/entity/PaymentEntity.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/exception/GlobalExceptionHandler.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/mapper/PaymentMapper.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/repository/PaymentRepository.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/service/impl/PaymentServiceImpl.class: Service resource file.
- api/target/classes/com/barclays/uscb/paymentservice/service/PaymentService.class: Service resource file.
- api/target/classes/openapi/openapi-spec.yaml: OpenAPI specification.
- api/target/maven-archiver/pom.properties: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- api/target/payment-service-api-0.0.1-SNAPSHOT.jar: Service resource file.
- api/target/payment-service-api-0.0.1-SNAPSHOT.jar.original: Service resource file.
- build.log: Service resource file.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/api/PaymentApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/model/PaymentHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/model/PaymentMethodsRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/model/PaymentsRecord.java: Java source file.
- oasgen/target/classes/com/barclays/uscb/paymentservice/api/PaymentApi.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/paymentservice/invoker/ApiClient.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/paymentservice/model/PaymentHealthResponse.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/paymentservice/model/PaymentMethodsRecord.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/paymentservice/model/PaymentsRecord.class: Service resource file.
- oasgen/target/maven-archiver/pom.properties: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- oasgen/target/payment-service-oasgen-0.0.1-SNAPSHOT.jar: Service resource file.
- pom.xml: Maven project configuration.
- README.md: Documentation file.
- service_context.json: JSON resource file.
```

### API Endpoints
- GET /health: Service health check
- GET /payments: Fetch payments
- GET /payment-methods: Fetch payment_methods

### Key Tables
- payments
- payment_methods
