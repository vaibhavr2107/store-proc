## ProductcatalogService

- Domain: productCatalog
- Owned Tables: inventory, products
- Dependencies: None
- Summary: ProductcatalogService coordinates productCatalog domain responsibilities across tables inventory, products.

### Overview
ProductcatalogService coordinates productCatalog domain responsibilities across tables inventory, products.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/productcatalogservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/controller/ProductcatalogController.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/entity/ProductcatalogEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/mapper/ProductcatalogMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/repository/ProductcatalogRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/service/impl/ProductcatalogServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/productcatalogservice/service/ProductcatalogService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/productcatalogservice/api/ProductcatalogApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/productcatalogservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/productcatalogservice/model/InventoryRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/productcatalogservice/model/ProductcatalogHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/productcatalogservice/model/ProductsRecord.java: Java source file.
- pom.xml: Maven project configuration.
```

### API Endpoints
- GET /health: Service health check
- GET /inventory: Fetch inventory
- GET /products: Fetch products

### Key Tables
- inventory
- products
