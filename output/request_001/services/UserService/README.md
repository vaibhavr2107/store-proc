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
- api/target/classes/application.yml: Spring Boot application settings.
- api/target/classes/com/barclays/uscb/userservice/Application.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/controller/UserController.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/entity/UserEntity.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/exception/GlobalExceptionHandler.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/mapper/UserMapper.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/repository/UserRepository.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/service/impl/UserServiceImpl.class: Service resource file.
- api/target/classes/com/barclays/uscb/userservice/service/UserService.class: Service resource file.
- api/target/classes/openapi/openapi-spec.yaml: OpenAPI specification.
- api/target/maven-archiver/pom.properties: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- api/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- api/target/user-service-api-0.0.1-SNAPSHOT.jar: Service resource file.
- build.log: Service resource file.
- oasgen/pom.xml: Maven project configuration.
- oasgen/src/main/java/com/barclays/uscb/userservice/api/UserApi.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/userservice/invoker/ApiClient.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/userservice/model/CustomersRecord.java: Java source file.
- oasgen/src/main/java/com/barclays/uscb/userservice/model/UserHealthResponse.java: Java source file.
- oasgen/target/classes/com/barclays/uscb/userservice/api/UserApi.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/userservice/invoker/ApiClient.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/userservice/model/CustomersRecord.class: Service resource file.
- oasgen/target/classes/com/barclays/uscb/userservice/model/UserHealthResponse.class: Service resource file.
- oasgen/target/maven-archiver/pom.properties: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst: Service resource file.
- oasgen/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst: Service resource file.
- oasgen/target/user-service-oasgen-0.0.1-SNAPSHOT.jar: Service resource file.
- pom.xml: Maven project configuration.
- README.md: Documentation file.
- service_context.json: JSON resource file.
```

### API Endpoints
- GET /health: Service health check
- GET /customers: Fetch customers

### Key Tables
- customers
