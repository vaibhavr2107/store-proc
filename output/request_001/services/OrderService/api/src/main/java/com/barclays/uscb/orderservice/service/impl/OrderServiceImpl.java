package com.barclays.uscb.orderservice.service.impl;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.barclays.uscb.orderservice.invoker.ApiClient;
import com.barclays.uscb.orderservice.model.OrderHealthResponse;
import com.barclays.uscb.orderservice.service.OrderService;

@Service
public class OrderServiceImpl implements OrderService {

    @Override
    public OrderHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getOrders() {
        return Collections.emptyList();
    }

    @Override
    public List<Map<String, Object>> getDelivery() {
        return Collections.emptyList();
    }
}
