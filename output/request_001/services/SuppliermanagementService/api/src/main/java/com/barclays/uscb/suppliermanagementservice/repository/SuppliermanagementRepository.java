package com.barclays.uscb.suppliermanagementservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.suppliermanagementservice.entity.SuppliermanagementEntity;

public interface SuppliermanagementRepository extends JpaRepository<SuppliermanagementEntity, String> {
}
