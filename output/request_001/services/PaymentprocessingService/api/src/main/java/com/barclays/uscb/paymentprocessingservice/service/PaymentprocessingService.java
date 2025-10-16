package com.barclays.uscb.paymentprocessingservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;

public interface PaymentprocessingService {

    PaymentprocessingHealthResponse health();

    List<Map<String, Object>> getPayments();
}
