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
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/api/PaymentApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentservice/model/PaymentHealthResponse.java: Java source file.
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
