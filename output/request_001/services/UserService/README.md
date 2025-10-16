## UserService

- Domain: user
- Owned Tables: customers
- Dependencies: None
- Summary: UserService coordinates user domain responsibilities across tables customers.

### Overview
UserService coordinates user domain responsibilities across tables customers.

### Directory Structure
```
- api/pom.xml: Maven project configuration.
- api/src/main/java/com/barclays/uscb/userservice/Application.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/controller/UserController.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/entity/UserEntity.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/exception/GlobalExceptionHandler.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/mapper/UserMapper.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/repository/UserRepository.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/service/impl/UserServiceImpl.java: Java source file.
- api/src/main/java/com/barclays/uscb/userservice/service/UserService.java: Java source file.
- api/src/main/resources/application.yml: Spring Boot application settings.
- api/src/main/resources/openapi/openapi-spec.yaml: OpenAPI specification.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/userservice/api/UserApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/userservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/userservice/model/UserHealthResponse.java: Java source file.
- pom.xml: Maven project configuration.
- README.md: Documentation file.
- service_context.json: JSON resource file.
```

### API Endpoints
- GET /health: Service health check
- GET /customers: Fetch customers

### Key Tables
- customers
