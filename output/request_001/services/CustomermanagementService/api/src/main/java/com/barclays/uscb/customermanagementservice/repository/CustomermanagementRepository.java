package com.barclays.uscb.customermanagementservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.customermanagementservice.entity.CustomermanagementEntity;

public interface CustomermanagementRepository extends JpaRepository<CustomermanagementEntity, String> {
}
