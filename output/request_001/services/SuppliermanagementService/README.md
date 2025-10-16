## SuppliermanagementService

- Domain: supplierManagement
- Owned Tables: suppliers
- Dependencies: None
- Summary: SuppliermanagementService coordinates supplierManagement domain responsibilities across tables suppliers.

### Overview
SuppliermanagementService coordinates supplierManagement domain responsibilities across tables suppliers.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/controller/SuppliermanagementController.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/entity/SuppliermanagementEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/mapper/SuppliermanagementMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/repository/SuppliermanagementRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/service/impl/SuppliermanagementServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/suppliermanagementservice/service/SuppliermanagementService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/suppliermanagementservice/api/SuppliermanagementApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/suppliermanagementservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/suppliermanagementservice/model/SuppliermanagementHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/suppliermanagementservice/model/SuppliersRecord.java: Java source file.
- pom.xml: Maven project configuration.
```

### API Endpoints
- GET /health: Service health check
- GET /suppliers: Fetch suppliers

### Key Tables
- suppliers
