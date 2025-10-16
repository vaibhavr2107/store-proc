package com.barclays.uscb.ordermanagementservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static OrdermanagementHealthResponse healthResponse(String status) {
        OrdermanagementHealthResponse response = new OrdermanagementHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
