package com.barclays.uscb.customermanagementservice.mapper;

import java.time.OffsetDateTime;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import com.barclays.uscb.customermanagementservice.entity.CustomermanagementEntity;
import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;

public final class CustomermanagementMapper {

    private CustomermanagementMapper() {
    }

    public static CustomermanagementHealthResponse toHealthResponse(CustomermanagementEntity entity) {
        CustomermanagementHealthResponse response = new CustomermanagementHealthResponse();
        response.setStatus(entity != null ? "UP" : "UNKNOWN");
        response.setTimestamp(OffsetDateTime.now());
        return response;
    }

    public static Map<String, Object> toMap(CustomermanagementEntity entity) {
        if (entity == null) {
            return Collections.emptyMap();
        }
        Map<String, Object> target = new LinkedHashMap<>();
        target.put("operation", entity.getOperation());
        target.put("record_id", entity.getRecordId());
        target.put("table_name", entity.getTableName());
        target.put("timestamp", entity.getTimestamp());
        target.put("user_id", entity.getUserId());
        return target;
    }

    public static CustomermanagementEntity fromMap(Map<String, Object> source) {
        CustomermanagementEntity entity = new CustomermanagementEntity();
        if (source == null) {
            return entity;
        }
        if (source.containsKey("operation")) {
            entity.setOperation(String.valueOf(source.get("operation")));
        }
        if (source.containsKey("record_id")) {
            entity.setRecordId(String.valueOf(source.get("record_id")));
        }
        if (source.containsKey("table_name")) {
            entity.setTableName(String.valueOf(source.get("table_name")));
        }
        if (source.containsKey("timestamp")) {
            entity.setTimestamp(String.valueOf(source.get("timestamp")));
        }
        if (source.containsKey("user_id")) {
            entity.setUserId(String.valueOf(source.get("user_id")));
        }
        return entity;
    }
}
