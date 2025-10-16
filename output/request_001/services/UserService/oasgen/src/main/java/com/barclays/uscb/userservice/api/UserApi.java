package com.barclays.uscb.userservice.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.barclays.uscb.userservice.model.UserHealthResponse;

@RequestMapping("/health")
public interface UserApi {

    @GetMapping
    ResponseEntity<UserHealthResponse> healthCheck();
}
