package com.barclays.uscb.orderservice.api;

import com.barclays.uscb.orderservice.model.OrderHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface OrderApi {

    @GetMapping("/health")
    ResponseEntity<OrderHealthResponse> orderServiceHealth();

    @GetMapping("/orders")
    ResponseEntity<List<Map<String, Object>>> getOrders();

    @GetMapping("/delivery")
    ResponseEntity<List<Map<String, Object>>> getDelivery();
}
