package com.barclays.uscb.paymentservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static PaymentHealthResponse healthResponse(String status) {
        PaymentHealthResponse response = new PaymentHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
