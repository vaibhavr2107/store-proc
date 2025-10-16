package com.barclays.uscb.orderservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.orderservice.model.OrderHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static OrderHealthResponse healthResponse(String status) {
        OrderHealthResponse response = new OrderHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
