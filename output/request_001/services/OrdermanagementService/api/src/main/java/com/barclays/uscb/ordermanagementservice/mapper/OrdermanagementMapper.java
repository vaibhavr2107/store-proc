package com.barclays.uscb.ordermanagementservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import com.barclays.uscb.ordermanagementservice.entity.OrdermanagementEntity;
import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;

public final class OrdermanagementMapper {

    private OrdermanagementMapper() {
    }

    public static OrdermanagementHealthResponse toHealthResponse(OrdermanagementEntity entity) {
        OrdermanagementHealthResponse response = new OrdermanagementHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(OrdermanagementEntity entity) {
        if (entity == null) {
            return Collections.emptyMap();
        }
        Map<String, Object> target = new LinkedHashMap<>();
        target.put("product_id", entity.getProductId());
        target.put("quantity", entity.getQuantity());
        target.put("unit_price", entity.getUnitPrice());
        return target;
    }

    public static OrdermanagementEntity fromMap(Map<String, Object> source) {
        OrdermanagementEntity entity = new OrdermanagementEntity();
        if (source == null) {
            return entity;
        }
        if (source.containsKey("product_id")) {
            entity.setProductId(String.valueOf(source.get("product_id")));
        }
        if (source.containsKey("quantity")) {
            entity.setQuantity(String.valueOf(source.get("quantity")));
        }
        if (source.containsKey("unit_price")) {
            entity.setUnitPrice(String.valueOf(source.get("unit_price")));
        }
        return entity;
    }
}
