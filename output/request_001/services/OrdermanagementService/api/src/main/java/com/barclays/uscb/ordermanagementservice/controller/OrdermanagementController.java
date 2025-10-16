package com.barclays.uscb.ordermanagementservice.controller;

import com.barclays.uscb.ordermanagementservice.api.OrdermanagementApi;
import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;
import com.barclays.uscb.ordermanagementservice.service.OrdermanagementService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class OrdermanagementController implements OrdermanagementApi {

    private final OrdermanagementService ordermanagementService;

    public OrdermanagementController(OrdermanagementService ordermanagementService) {
        this.ordermanagementService = ordermanagementService;
    }

    @GetMapping("/health")
    public ResponseEntity<OrdermanagementHealthResponse> ordermanagementServiceHealth() {
        return ResponseEntity.ok(ordermanagementService.health());
    }

    @GetMapping("/order-items")
    public ResponseEntity<List<Map<String, Object>>> getOrderItems() {
        return ResponseEntity.ok(ordermanagementService.getOrderItems());
    }

    @GetMapping("/orders")
    public ResponseEntity<List<Map<String, Object>>> getOrders() {
        return ResponseEntity.ok(ordermanagementService.getOrders());
    }
}
