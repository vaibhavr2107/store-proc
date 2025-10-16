package com.barclays.uscb.customermanagementservice.api;

import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface CustomermanagementApi {

    @GetMapping("/health")
    ResponseEntity<CustomermanagementHealthResponse> customermanagementServiceHealth();

    @PostMapping("/audit-logs")
    ResponseEntity<Map<String, Object>> createAuditLogs(@RequestBody Map<String, Object> body);

    @GetMapping("/customers")
    ResponseEntity<List<Map<String, Object>>> getCustomers();

    @PutMapping("/customers/{address}")
    ResponseEntity<Map<String, Object>> updateCustomers(@PathVariable("address") String address, @RequestBody Map<String, Object> body);
}
