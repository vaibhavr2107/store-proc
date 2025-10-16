package com.barclays.uscb.userservice.controller;

import com.barclays.uscb.userservice.api.UserApi;
import com.barclays.uscb.userservice.model.UserHealthResponse;
import com.barclays.uscb.userservice.service.UserService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class UserController implements UserApi {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/health")
    public ResponseEntity<UserHealthResponse> userServiceHealth() {
        return ResponseEntity.ok(userService.health());
    }

    @GetMapping("/customers")
    public ResponseEntity<List<Map<String, Object>>> getCustomers() {
        return ResponseEntity.ok(userService.getCustomers());
    }
}
