package com.barclays.uscb.paymentprocessingservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.paymentprocessingservice.entity.PaymentprocessingEntity;

public interface PaymentprocessingRepository extends JpaRepository<PaymentprocessingEntity, String> {
}
