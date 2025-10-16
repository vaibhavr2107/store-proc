package com.barclays.uscb.productcatalogservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;

public interface ProductcatalogService {

    ProductcatalogHealthResponse health();

    List<Map<String, Object>> getInventory();

    List<Map<String, Object>> getProducts();
}
