package com.barclays.uscb.orderservice.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.barclays.uscb.orderservice.model.OrderHealthResponse;

@RequestMapping("/health")
public interface OrderApi {

    @GetMapping
    ResponseEntity<OrderHealthResponse> healthCheck();
}
