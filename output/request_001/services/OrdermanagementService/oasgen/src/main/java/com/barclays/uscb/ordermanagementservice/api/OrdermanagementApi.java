package com.barclays.uscb.ordermanagementservice.api;

import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface OrdermanagementApi {

    @GetMapping("/health")
    ResponseEntity<OrdermanagementHealthResponse> ordermanagementServiceHealth();

    @GetMapping("/order-items")
    ResponseEntity<List<Map<String, Object>>> getOrderItems();

    @GetMapping("/orders")
    ResponseEntity<List<Map<String, Object>>> getOrders();
}
