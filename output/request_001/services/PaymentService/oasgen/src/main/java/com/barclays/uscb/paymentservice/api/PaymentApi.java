package com.barclays.uscb.paymentservice.api;

import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface PaymentApi {

    @GetMapping("/health")
    ResponseEntity<PaymentHealthResponse> paymentServiceHealth();

    @GetMapping("/payments")
    ResponseEntity<List<Map<String, Object>>> getPayments();

    @GetMapping("/payment-methods")
    ResponseEntity<List<Map<String, Object>>> getPaymentMethods();
}
