package com.barclays.uscb.orderservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.orderservice.model.OrderHealthResponse;

public interface OrderService {

    OrderHealthResponse health();

    List<Map<String, Object>> getOrders();

    List<Map<String, Object>> getDelivery();
}
