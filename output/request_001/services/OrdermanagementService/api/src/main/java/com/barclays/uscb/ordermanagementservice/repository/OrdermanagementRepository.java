package com.barclays.uscb.ordermanagementservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.ordermanagementservice.entity.OrdermanagementEntity;

public interface OrdermanagementRepository extends JpaRepository<OrdermanagementEntity, String> {
}
