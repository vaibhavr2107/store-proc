package com.barclays.uscb.suppliermanagementservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static SuppliermanagementHealthResponse healthResponse(String status) {
        SuppliermanagementHealthResponse response = new SuppliermanagementHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
