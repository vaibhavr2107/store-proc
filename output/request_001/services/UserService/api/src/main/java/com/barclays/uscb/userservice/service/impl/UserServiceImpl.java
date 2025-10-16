package com.barclays.uscb.userservice.service.impl;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.barclays.uscb.userservice.invoker.ApiClient;
import com.barclays.uscb.userservice.model.UserHealthResponse;
import com.barclays.uscb.userservice.service.UserService;

@Service
public class UserServiceImpl implements UserService {

    @Override
    public UserHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getCustomers() {
        return Collections.emptyList();
    }
}
