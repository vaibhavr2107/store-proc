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
- api/target/classes/application.yml: Spring Boot application settings.
- api/target/classes/com/barclays/uscb/orderservice/Application.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/controller/OrderController.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/entity/OrderEntity.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/exception/GlobalExceptionHandler.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/mapper/OrderMapper.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/repository/OrderRepository.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/service/impl/OrderServiceImpl.class: Service resource file.
- api/target/classes/com/barclays/uscb/orderservice/service/OrderService.class: Service resource file.
- api/target/classes/openapi/openapi-spec.yaml: OpenAPI specification.
- api/target/maven-archiver/pom.properties: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- api/target/order-service-api-0.0.1-SNAPSHOT.jar: Service resource file.
- api/target/order-service-api-0.0.1-SNAPSHOT.jar.original: Service resource file.
- build.log: Service resource file.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/orderservice/api/OrderApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/model/DeliveryRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/model/InvoicesRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/model/OrderHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/orderservice/model/OrdersRecord.java: Java source file.
- oasgen/target/classes/com/barclays/uscb/orderservice/api/OrderApi.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/orderservice/invoker/ApiClient.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/orderservice/model/DeliveryRecord.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/orderservice/model/InvoicesRecord.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/orderservice/model/OrderHealthResponse.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/orderservice/model/OrdersRecord.class: Service resource file.
- oasgen/target/maven-archiver/pom.properties: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- oasgen/target/order-service-oasgen-0.0.1-SNAPSHOT.jar: Service resource file.
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
