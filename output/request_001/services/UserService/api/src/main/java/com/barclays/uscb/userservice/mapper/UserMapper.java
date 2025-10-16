package com.barclays.uscb.userservice.mapper;

import java.util.Collections;
import java.util.Map;

import com.barclays.uscb.userservice.entity.UserEntity;
import com.barclays.uscb.userservice.model.UserHealthResponse;

public final class UserMapper {

    private UserMapper() {
    }

    public static UserHealthResponse toHealthResponse(UserEntity entity) {
        UserHealthResponse response = new UserHealthResponse();
        response.setStatus(entity != null ? entity.getStatus() : "UNKNOWN");
        return response;
    }

    public static Map<String, Object> toMap(UserEntity entity) {
        return Collections.emptyMap();
    }
}
