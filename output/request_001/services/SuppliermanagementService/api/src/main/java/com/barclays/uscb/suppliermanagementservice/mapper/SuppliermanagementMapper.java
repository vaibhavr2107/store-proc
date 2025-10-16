package com.barclays.uscb.suppliermanagementservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import com.barclays.uscb.suppliermanagementservice.entity.SuppliermanagementEntity;
import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;

public final class SuppliermanagementMapper {

    private SuppliermanagementMapper() {
    }

    public static SuppliermanagementHealthResponse toHealthResponse(SuppliermanagementEntity entity) {
        SuppliermanagementHealthResponse response = new SuppliermanagementHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(SuppliermanagementEntity entity) {
        if (entity == null) {
            return Collections.emptyMap();
        }
        Map<String, Object> target = new LinkedHashMap<>();
        target.put("contact_email", entity.getContactEmail());
        target.put("supplier_name", entity.getSupplierName());
        return target;
    }

    public static SuppliermanagementEntity fromMap(Map<String, Object> source) {
        SuppliermanagementEntity entity = new SuppliermanagementEntity();
        if (source == null) {
            return entity;
        }
        if (source.containsKey("contact_email")) {
            entity.setContactEmail(String.valueOf(source.get("contact_email")));
        }
        if (source.containsKey("supplier_name")) {
            entity.setSupplierName(String.valueOf(source.get("supplier_name")));
        }
        return entity;
    }
}
