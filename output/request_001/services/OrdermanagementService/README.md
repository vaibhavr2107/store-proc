## OrdermanagementService

- Domain: orderManagement
- Owned Tables: order_items, orders
- Dependencies: productCatalog, supplierManagement
- Summary: OrdermanagementService coordinates orderManagement domain responsibilities across tables order_items, orders.

### Overview
OrdermanagementService coordinates orderManagement domain responsibilities across tables order_items, orders.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/controller/OrdermanagementController.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/entity/OrdermanagementEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/mapper/OrdermanagementMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/repository/OrdermanagementRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/service/impl/OrdermanagementServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/ordermanagementservice/service/OrdermanagementService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/ordermanagementservice/api/OrdermanagementApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/ordermanagementservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/ordermanagementservice/model/OrderItemsRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/ordermanagementservice/model/OrdermanagementHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/ordermanagementservice/model/OrdersRecord.java: Java source file.
- pom.xml: Maven project configuration.
```

### API Endpoints
- GET /health: Service health check
- GET /order-items: Fetch order_items
- GET /orders: Fetch orders

### Key Tables
- order_items
- orders
