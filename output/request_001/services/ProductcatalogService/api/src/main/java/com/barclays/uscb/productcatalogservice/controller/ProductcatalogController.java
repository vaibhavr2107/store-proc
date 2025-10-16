package com.barclays.uscb.productcatalogservice.controller;

import com.barclays.uscb.productcatalogservice.api.ProductcatalogApi;
import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;
import com.barclays.uscb.productcatalogservice.service.ProductcatalogService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class ProductcatalogController implements ProductcatalogApi {

    private final ProductcatalogService productcatalogService;

    public ProductcatalogController(ProductcatalogService productcatalogService) {
        this.productcatalogService = productcatalogService;
    }

    @GetMapping("/health")
    public ResponseEntity<ProductcatalogHealthResponse> productcatalogServiceHealth() {
        return ResponseEntity.ok(productcatalogService.health());
    }

    @GetMapping("/inventory")
    public ResponseEntity<List<Map<String, Object>>> getInventory() {
        return ResponseEntity.ok(productcatalogService.getInventory());
    }

    @GetMapping("/products")
    public ResponseEntity<List<Map<String, Object>>> getProducts() {
        return ResponseEntity.ok(productcatalogService.getProducts());
    }
}
