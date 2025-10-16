## CustomermanagementService

- Domain: customerManagement
- Owned Tables: audit_logs, customers
- Dependencies: None
- Summary: CustomermanagementService coordinates customerManagement domain responsibilities across tables audit_logs, customers.

### Overview
CustomermanagementService coordinates customerManagement domain responsibilities across tables audit_logs, customers.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/customermanagementservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/controller/CustomermanagementController.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/entity/CustomermanagementEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/mapper/CustomermanagementMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/repository/CustomermanagementRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/service/CustomermanagementService.java: Java source file.
- api/src/main/java/com/barclays/uscb/customermanagementservice/service/impl/CustomermanagementServiceImpl.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/customermanagementservice/api/CustomermanagementApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/customermanagementservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/customermanagementservice/model/AuditLogsRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/customermanagementservice/model/CustomermanagementHealthResponse.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/customermanagementservice/model/CustomersRecord.java: Java source file.
- pom.xml: Maven project configuration.
```

### API Endpoints
- GET /health: Service health check
- POST /audit-logs: Create audit_logs
- GET /customers: Fetch customers
- PUT /customers/{address}: Update customers

### Key Tables
- audit_logs
- customers
