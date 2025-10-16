package com.barclays.uscb.orderservice.mapper;

import java.util.Collections;
import java.util.Map;

import com.barclays.uscb.orderservice.entity.OrderEntity;
import com.barclays.uscb.orderservice.model.OrderHealthResponse;

public final class OrderMapper {

    private OrderMapper() {
    }

    public static OrderHealthResponse toHealthResponse(OrderEntity entity) {
        OrderHealthResponse response = new OrderHealthResponse();
        response.setStatus(entity != null ? entity.getStatus() : "UNKNOWN");
        return response;
    }

    public static Map<String, Object> toMap(OrderEntity entity) {
        return Collections.emptyMap();
    }
}
