package com.barclays.uscb.paymentservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;

public interface PaymentService {

    PaymentHealthResponse health();

    List<Map<String, Object>> getPayments();

    List<Map<String, Object>> getPaymentMethods();
}
