package com.barclays.uscb.ordermanagementservice.service.impl;

import com.barclays.uscb.ordermanagementservice.entity.OrdermanagementEntity;
import com.barclays.uscb.ordermanagementservice.invoker.ApiClient;
import com.barclays.uscb.ordermanagementservice.mapper.OrdermanagementMapper;
import com.barclays.uscb.ordermanagementservice.model.OrdermanagementHealthResponse;
import com.barclays.uscb.ordermanagementservice.repository.OrdermanagementRepository;
import com.barclays.uscb.ordermanagementservice.service.OrdermanagementService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class OrdermanagementServiceImpl implements OrdermanagementService {

    private final OrdermanagementRepository ordermanagementRepository;

    public OrdermanagementServiceImpl(OrdermanagementRepository ordermanagementRepository) {
        this.ordermanagementRepository = ordermanagementRepository;
    }

    @Override
    public OrdermanagementHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getOrderItems() {
        return ordermanagementRepository
                .findAll()
                .stream()
                .map(OrdermanagementMapper::toMap)
                .collect(Collectors.toList());
    }

    @Override
    public List<Map<String, Object>> getOrders() {
        // TODO implement lookup using downstream client for table orders
        return Collections.emptyList();
    }
}
