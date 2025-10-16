package com.barclays.uscb.productcatalogservice.api;

import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface ProductcatalogApi {

    @GetMapping("/health")
    ResponseEntity<ProductcatalogHealthResponse> productcatalogServiceHealth();

    @GetMapping("/inventory")
    ResponseEntity<List<Map<String, Object>>> getInventory();

    @GetMapping("/products")
    ResponseEntity<List<Map<String, Object>>> getProducts();
}
