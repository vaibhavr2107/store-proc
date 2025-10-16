package com.barclays.uscb.paymentprocessingservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static PaymentprocessingHealthResponse healthResponse(String status) {
        PaymentprocessingHealthResponse response = new PaymentprocessingHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
