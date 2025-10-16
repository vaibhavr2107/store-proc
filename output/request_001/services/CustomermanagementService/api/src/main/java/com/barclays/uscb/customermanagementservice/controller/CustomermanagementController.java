package com.barclays.uscb.customermanagementservice.controller;

import com.barclays.uscb.customermanagementservice.api.CustomermanagementApi;
import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;
import com.barclays.uscb.customermanagementservice.service.CustomermanagementService;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class CustomermanagementController implements CustomermanagementApi {

    private final CustomermanagementService customermanagementService;

    public CustomermanagementController(CustomermanagementService customermanagementService) {
        this.customermanagementService = customermanagementService;
    }

    @GetMapping("/health")
    public ResponseEntity<CustomermanagementHealthResponse> customermanagementServiceHealth() {
        return ResponseEntity.ok(customermanagementService.health());
    }

    @PostMapping("/audit-logs")
    public ResponseEntity<Map<String, Object>> createAuditLogs(@RequestBody Map<String, Object> body) {
        return ResponseEntity.status(HttpStatus.CREATED).body(customermanagementService.createAuditLogs(body));
    }

    @GetMapping("/customers")
    public ResponseEntity<List<Map<String, Object>>> getCustomers() {
        return ResponseEntity.ok(customermanagementService.getCustomers());
    }

    @PutMapping("/customers/{address}")
    public ResponseEntity<Map<String, Object>> updateCustomers(@PathVariable("address") String address, @RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(customermanagementService.updateCustomers(address, body));
    }
}
