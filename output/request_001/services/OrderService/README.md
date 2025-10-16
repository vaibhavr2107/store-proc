## OrderService

- Domain: order
- Owned Tables: orders, delivery, invoices
- Dependencies: None
- Summary: OrderService coordinates order domain responsibilities across tables orders, delivery, invoices.

### Overview
OrderService coordinates order domain responsibilities across tables orders, delivery, invoices.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/orderservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/controller/OrderController.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/entity/OrderEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/mapper/OrderMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/repository/OrderRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/service/impl/OrderServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/orderservice/service/OrderService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/orderservice/api/OrderApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/model/OrderHealthResponse.java: Java source file.
- pom.xml: Maven project configuration.
- README.md: Documentation file.
- service_context.json: JSON resource file.
```

### API Endpoints
- GET /health: Service health check
- GET /orders: Fetch orders
- GET /delivery: Fetch delivery

### Key Tables
- orders
- delivery
- invoices
