package com.barclays.uscb.customermanagementservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static CustomermanagementHealthResponse healthResponse(String status) {
        CustomermanagementHealthResponse response = new CustomermanagementHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
