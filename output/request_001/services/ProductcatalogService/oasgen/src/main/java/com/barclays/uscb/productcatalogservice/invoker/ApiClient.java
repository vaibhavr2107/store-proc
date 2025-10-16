package com.barclays.uscb.productcatalogservice.invoker;

import java.time.OffsetDateTime;

import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;

public final class ApiClient {

    private ApiClient() {
    }

    public static ProductcatalogHealthResponse healthResponse(String status) {
        ProductcatalogHealthResponse response = new ProductcatalogHealthResponse();
        response.setStatus(status);
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }
}
