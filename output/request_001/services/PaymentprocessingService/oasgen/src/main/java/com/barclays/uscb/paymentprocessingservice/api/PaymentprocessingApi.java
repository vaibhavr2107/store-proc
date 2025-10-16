package com.barclays.uscb.paymentprocessingservice.api;

import com.barclays.uscb.paymentprocessingservice.model.PaymentprocessingHealthResponse;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

public interface PaymentprocessingApi {

    @GetMapping("/health")
    ResponseEntity<PaymentprocessingHealthResponse> paymentprocessingServiceHealth();

    @GetMapping("/payments")
    ResponseEntity<List<Map<String, Object>>> getPayments();
}
