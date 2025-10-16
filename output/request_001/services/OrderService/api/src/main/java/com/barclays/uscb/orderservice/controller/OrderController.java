package com.barclays.uscb.orderservice.controller;

import com.barclays.uscb.orderservice.api.OrderApi;
import com.barclays.uscb.orderservice.model.OrderHealthResponse;
import com.barclays.uscb.orderservice.service.OrderService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class OrderController implements OrderApi {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/health")
    public ResponseEntity<OrderHealthResponse> orderServiceHealth() {
        return ResponseEntity.ok(orderService.health());
    }

    @GetMapping("/orders")
    public ResponseEntity<List<Map<String, Object>>> getOrders() {
        return ResponseEntity.ok(orderService.getOrders());
    }

    @GetMapping("/delivery")
    public ResponseEntity<List<Map<String, Object>>> getDelivery() {
        return ResponseEntity.ok(orderService.getDelivery());
    }
}
