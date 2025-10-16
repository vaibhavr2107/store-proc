package com.barclays.uscb.paymentservice.service.impl;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.barclays.uscb.paymentservice.invoker.ApiClient;
import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;
import com.barclays.uscb.paymentservice.service.PaymentService;

@Service
public class PaymentServiceImpl implements PaymentService {

    @Override
    public PaymentHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getPayments() {
        return Collections.emptyList();
    }

    @Override
    public List<Map<String, Object>> getPaymentMethods() {
        return Collections.emptyList();
    }
}
