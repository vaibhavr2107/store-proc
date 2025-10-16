package com.barclays.uscb.suppliermanagementservice.controller;

import com.barclays.uscb.suppliermanagementservice.api.SuppliermanagementApi;
import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;
import com.barclays.uscb.suppliermanagementservice.service.SuppliermanagementService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SuppliermanagementController implements SuppliermanagementApi {

    private final SuppliermanagementService suppliermanagementService;

    public SuppliermanagementController(SuppliermanagementService suppliermanagementService) {
        this.suppliermanagementService = suppliermanagementService;
    }

    @GetMapping("/health")
    public ResponseEntity<SuppliermanagementHealthResponse> suppliermanagementServiceHealth() {
        return ResponseEntity.ok(suppliermanagementService.health());
    }

    @GetMapping("/suppliers")
    public ResponseEntity<List<Map<String, Object>>> getSuppliers() {
        return ResponseEntity.ok(suppliermanagementService.getSuppliers());
    }
}
