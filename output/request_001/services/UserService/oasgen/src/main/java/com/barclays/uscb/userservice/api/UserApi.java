package com.barclays.uscb.userservice.api;

import com.barclays.uscb.userservice.model.UserHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface UserApi {

    @GetMapping("/health")
    ResponseEntity<UserHealthResponse> userServiceHealth();

    @GetMapping("/customers")
    ResponseEntity<List<Map<String, Object>>> getCustomers();
}
