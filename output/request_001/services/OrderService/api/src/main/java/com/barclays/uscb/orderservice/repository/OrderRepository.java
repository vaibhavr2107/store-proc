package com.barclays.uscb.orderservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.orderservice.entity.OrderEntity;

public interface OrderRepository extends JpaRepository<OrderEntity, String> {
}
