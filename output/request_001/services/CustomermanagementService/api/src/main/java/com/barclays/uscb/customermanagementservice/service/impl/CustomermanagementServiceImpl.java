package com.barclays.uscb.customermanagementservice.service.impl;

import com.barclays.uscb.customermanagementservice.entity.CustomermanagementEntity;
import com.barclays.uscb.customermanagementservice.invoker.ApiClient;
import com.barclays.uscb.customermanagementservice.mapper.CustomermanagementMapper;
import com.barclays.uscb.customermanagementservice.model.CustomermanagementHealthResponse;
import com.barclays.uscb.customermanagementservice.repository.CustomermanagementRepository;
import com.barclays.uscb.customermanagementservice.service.CustomermanagementService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class CustomermanagementServiceImpl implements CustomermanagementService {

    private final CustomermanagementRepository customermanagementRepository;

    public CustomermanagementServiceImpl(CustomermanagementRepository customermanagementRepository) {
        this.customermanagementRepository = customermanagementRepository;
    }

    @Override
    public CustomermanagementHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public Map<String, Object> createAuditLogs(Map<String, Object> body) {
        CustomermanagementEntity entity = CustomermanagementMapper.fromMap(body);
        CustomermanagementEntity saved = customermanagementRepository.save(entity);
        return CustomermanagementMapper.toMap(saved);
    }

    @Override
    public List<Map<String, Object>> getCustomers() {
        // TODO implement lookup using downstream client for table customers
        return Collections.emptyList();
    }

    @Override
    public Map<String, Object> updateCustomers(String address, Map<String, Object> body) {
        // TODO implement write logic for table customers
        return Collections.emptyMap();
    }
}
