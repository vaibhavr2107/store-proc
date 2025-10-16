package com.barclays.uscb.paymentprocessingservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import com.barclays.uscb.paymentprocessingservice.entity.PaymentprocessingEntity;
import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;

public final class PaymentprocessingMapper {

    private PaymentprocessingMapper() {
    }

    public static PaymentprocessingHealthResponse toHealthResponse(PaymentprocessingEntity entity) {
        PaymentprocessingHealthResponse response = new PaymentprocessingHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(PaymentprocessingEntity entity) {
        if (entity == null) {
            return Collections.emptyMap();
        }
        Map<String, Object> target = new LinkedHashMap<>();
        target.put("amount", entity.getAmount());
        target.put("order_id", entity.getOrderId());
        target.put("payment_date", entity.getPaymentDate());
        target.put("payment_id", entity.getPaymentId());
        target.put("payment_method", entity.getPaymentMethod());
        target.put("payment_status", entity.getPaymentStatus());
        return target;
    }

    public static PaymentprocessingEntity fromMap(Map<String, Object> source) {
        PaymentprocessingEntity entity = new PaymentprocessingEntity();
        if (source == null) {
            return entity;
        }
        if (source.containsKey("amount")) {
            entity.setAmount(String.valueOf(source.get("amount")));
        }
        if (source.containsKey("order_id")) {
            entity.setOrderId(String.valueOf(source.get("order_id")));
        }
        if (source.containsKey("payment_date")) {
            entity.setPaymentDate(String.valueOf(source.get("payment_date")));
        }
        if (source.containsKey("payment_id")) {
            entity.setPaymentId(String.valueOf(source.get("payment_id")));
        }
        if (source.containsKey("payment_method")) {
            entity.setPaymentMethod(String.valueOf(source.get("payment_method")));
        }
        if (source.containsKey("payment_status")) {
            entity.setPaymentStatus(String.valueOf(source.get("payment_status")));
        }
        return entity;
    }
}
