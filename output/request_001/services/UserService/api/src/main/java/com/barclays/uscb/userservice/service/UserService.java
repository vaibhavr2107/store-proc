package com.barclays.uscb.userservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.userservice.model.UserHealthResponse;

public interface UserService {

    UserHealthResponse health();

    List<Map<String, Object>> getCustomers();
}
