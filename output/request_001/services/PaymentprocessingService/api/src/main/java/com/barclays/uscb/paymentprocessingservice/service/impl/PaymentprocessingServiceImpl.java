package com.barclays.uscb.paymentprocessingservice.service.impl;

import com.barclays.uscb.paymentprocessingservice.entity.PaymentprocessingEntity;
import com.barclays.uscb.paymentprocessingservice.invoker.ApiClient;
import com.barclays.uscb.paymentprocessingservice.mapper.PaymentprocessingMapper;
import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;
import com.barclays.uscb.paymentprocessingservice.repository.PaymentprocessingRepository;
import com.barclays.uscb.paymentprocessingservice.service.PaymentprocessingService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class PaymentprocessingServiceImpl implements PaymentprocessingService {

    private final PaymentprocessingRepository paymentprocessingRepository;

    public PaymentprocessingServiceImpl(PaymentprocessingRepository paymentprocessingRepository) {
        this.paymentprocessingRepository = paymentprocessingRepository;
    }

    @Override
    public PaymentprocessingHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getPayments() {
        return paymentprocessingRepository
                .findAll()
                .stream()
                .map(PaymentprocessingMapper::toMap)
                .collect(Collectors.toList());
    }
}
