package com.barclays.uscb.userservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.userservice.model.UserHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static UserHealthResponse healthResponse(String status) {
        UserHealthResponse response = new UserHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
