package com.barclays.uscb.productcatalogservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import com.barclays.uscb.productcatalogservice.entity.ProductcatalogEntity;
import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;

public final class ProductcatalogMapper {

    private ProductcatalogMapper() {
    }

    public static ProductcatalogHealthResponse toHealthResponse(ProductcatalogEntity entity) {
        ProductcatalogHealthResponse response = new ProductcatalogHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(ProductcatalogEntity entity) {
        if (entity == null) {
            return Collections.emptyMap();
        }
        Map<String, Object> target = new LinkedHashMap<>();
        target.put("stock_quantity", entity.getStockQuantity());
        return target;
    }

    public static ProductcatalogEntity fromMap(Map<String, Object> source) {
        ProductcatalogEntity entity = new ProductcatalogEntity();
        if (source == null) {
            return entity;
        }
        if (source.containsKey("stock_quantity")) {
            entity.setStockQuantity(String.valueOf(source.get("stock_quantity")));
        }
        return entity;
    }
}
