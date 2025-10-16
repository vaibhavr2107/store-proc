package com.barclays.uscb.ordermanagementservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;

public interface OrdermanagementService {

    OrdermanagementHealthResponse health();

    List<Map<String, Object>> getOrderItems();

    List<Map<String, Object>> getOrders();
}
