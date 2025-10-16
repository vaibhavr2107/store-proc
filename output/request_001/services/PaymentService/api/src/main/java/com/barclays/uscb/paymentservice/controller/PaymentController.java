package com.barclays.uscb.paymentservice.controller;

import com.barclays.uscb.paymentservice.api.PaymentApi;
import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;
import com.barclays.uscb.paymentservice.service.PaymentService;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class PaymentController implements PaymentApi {

    private final PaymentService paymentService;

    public PaymentController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @GetMapping("/health")
    public ResponseEntity<PaymentHealthResponse> paymentServiceHealth() {
        return ResponseEntity.ok(paymentService.health());
    }

    @GetMapping("/payments")
    public ResponseEntity<List<Map<String, Object>>> getPayments() {
        return ResponseEntity.ok(paymentService.getPayments());
    }

    @GetMapping("/payment-methods")
    public ResponseEntity<List<Map<String, Object>>> getPaymentMethods() {
        return ResponseEntity.ok(paymentService.getPaymentMethods());
    }
}
