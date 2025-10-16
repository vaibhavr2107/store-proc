package com.barclays.uscb.customermanagementservice.model;

import java.time.OffsetDateTime;

public class CustomermanagementHealthResponse {

    private String status;
    private OffsetDateTime timestamp = OffsetDateTime.now();

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public OffsetDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(OffsetDateTime timestamp) {
        this.timestamp = timestamp;
    }
}
