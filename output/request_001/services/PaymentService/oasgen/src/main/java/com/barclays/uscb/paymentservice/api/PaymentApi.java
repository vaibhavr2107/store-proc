package com.barclays.uscb.paymentservice.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.barclays.uscb.paymentservice.model.PaymentHealthResponse;

@RequestMapping("/health")
public interface PaymentApi {

    @GetMapping
    ResponseEntity<PaymentHealthResponse> healthCheck();
}
