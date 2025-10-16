package com.barclays.uscb.paymentservice.mapper;

import java.util.Collections;
import java.util.Map;

import com.barclays.uscb.paymentservice.entity.PaymentEntity;
import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;

public final class PaymentMapper {

    private PaymentMapper() {
    }

    public static PaymentHealthResponse toHealthResponse(PaymentEntity entity) {
        PaymentHealthResponse response = new PaymentHealthResponse();
        response.setStatus(entity != null ? entity.getStatus() : "UNKNOWN");
        return response;
    }

    public static Map<String, Object> toMap(PaymentEntity entity) {
        return Collections.emptyMap();
    }
}
