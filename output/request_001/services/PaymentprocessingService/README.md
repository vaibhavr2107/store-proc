## PaymentprocessingService

- Domain: paymentProcessing
- Owned Tables: payments
- Dependencies: orderManagement
- Summary: PaymentprocessingService coordinates paymentProcessing domain responsibilities across tables payments.

### Overview
PaymentprocessingService coordinates paymentProcessing domain responsibilities across tables payments.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/controller/PaymentprocessingController.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/entity/PaymentprocessingEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/mapper/PaymentprocessingMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/repository/PaymentprocessingRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/service/impl/PaymentprocessingServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/paymentprocessingservice/service/PaymentprocessingService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/paymentprocessingservice/api/PaymentprocessingApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentprocessingservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentprocessingservice/model/PaymentprocessingHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/paymentprocessingservice/model/PaymentsRecord.java: Java source file.
- pom.xml: Maven project configuration.
```

### API Endpoints
- GET /health: Service health check
- GET /payments: Fetch payments

### Key Tables
- payments
