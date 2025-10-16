package com.barclays.uscb.paymentservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.paymentservice.entity.PaymentEntity;

public interface PaymentRepository extends JpaRepository<PaymentEntity, String> {
}
