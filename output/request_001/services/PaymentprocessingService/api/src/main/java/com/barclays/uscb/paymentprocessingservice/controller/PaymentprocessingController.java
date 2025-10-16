package com.barclays.uscb.paymentprocessingservice.controller;

import com.barclays.uscb.paymentprocessingservice.api.PaymentprocessingApi;
import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;
import com.barclays.uscb.paymentprocessingservice.service.PaymentprocessingService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class PaymentprocessingController implements PaymentprocessingApi {

    private final PaymentprocessingService paymentprocessingService;

    public PaymentprocessingController(PaymentprocessingService paymentprocessingService) {
        this.paymentprocessingService = paymentprocessingService;
    }

    @GetMapping("/health")
    public ResponseEntity<PaymentprocessingHealthResponse> paymentprocessingServiceHealth() {
        return ResponseEntity.ok(paymentprocessingService.health());
    }

    @GetMapping("/payments")
    public ResponseEntity<List<Map<String, Object>>> getPayments() {
        return ResponseEntity.ok(paymentprocessingService.getPayments());
    }
}
