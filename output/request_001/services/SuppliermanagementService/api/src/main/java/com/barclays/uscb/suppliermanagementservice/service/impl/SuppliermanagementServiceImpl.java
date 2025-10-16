package com.barclays.uscb.suppliermanagementservice.service.impl;

import com.barclays.uscb.suppliermanagementservice.entity.SuppliermanagementEntity;
import com.barclays.uscb.suppliermanagementservice.invoker.ApiClient;
import com.barclays.uscb.suppliermanagementservice.mapper.SuppliermanagementMapper;
import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;
import com.barclays.uscb.suppliermanagementservice.repository.SuppliermanagementRepository;
import com.barclays.uscb.suppliermanagementservice.service.SuppliermanagementService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class SuppliermanagementServiceImpl implements SuppliermanagementService {

    private final SuppliermanagementRepository suppliermanagementRepository;

    public SuppliermanagementServiceImpl(SuppliermanagementRepository suppliermanagementRepository) {
        this.suppliermanagementRepository = suppliermanagementRepository;
    }

    @Override
    public SuppliermanagementHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getSuppliers() {
        return suppliermanagementRepository
                .findAll()
                .stream()
                .map(SuppliermanagementMapper::toMap)
                .collect(Collectors.toList());
    }
}
