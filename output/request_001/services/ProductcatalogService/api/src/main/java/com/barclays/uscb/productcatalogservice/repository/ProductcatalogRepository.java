package com.barclays.uscb.productcatalogservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.productcatalogservice.entity.ProductcatalogEntity;

public interface ProductcatalogRepository extends JpaRepository<ProductcatalogEntity, String> {
}
