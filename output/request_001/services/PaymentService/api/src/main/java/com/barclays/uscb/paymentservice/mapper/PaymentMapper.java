package com.barclays.uscb.paymentservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.Map;

import com.barclays.uscb.paymentservice.entity.PaymentEntity;
import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;

public final class PaymentMapper {

    private PaymentMapper() {
    }

    public static PaymentHealthResponse toHealthResponse(PaymentEntity entity) {
        PaymentHealthResponse response = new PaymentHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(PaymentEntity entity) {
        return Collections.emptyMap();
    }
}
