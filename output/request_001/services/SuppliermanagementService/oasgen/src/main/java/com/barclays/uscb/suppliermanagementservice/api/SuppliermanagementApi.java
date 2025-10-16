package com.barclays.uscb.suppliermanagementservice.api;

import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface SuppliermanagementApi {

    @GetMapping("/health")
    ResponseEntity<SuppliermanagementHealthResponse> suppliermanagementServiceHealth();

    @GetMapping("/suppliers")
    ResponseEntity<List<Map<String, Object>>> getSuppliers();
}
