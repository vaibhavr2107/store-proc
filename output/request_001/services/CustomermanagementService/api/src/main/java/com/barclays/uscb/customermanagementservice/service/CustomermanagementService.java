package com.barclays.uscb.customermanagementservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;

public interface CustomermanagementService {

    CustomermanagementHealthResponse health();

    Map<String, Object> createAuditLogs(Map<String, Object> body);

    List<Map<String, Object>> getCustomers();

    Map<String, Object> updateCustomers(String address, Map<String, Object> body);
}
