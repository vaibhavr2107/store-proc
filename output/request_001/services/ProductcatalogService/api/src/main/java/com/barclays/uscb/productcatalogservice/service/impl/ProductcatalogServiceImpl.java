package com.barclays.uscb.productcatalogservice.service.impl;

import com.barclays.uscb.productcatalogservice.entity.ProductcatalogEntity;
import com.barclays.uscb.productcatalogservice.invoker.ApiClient;
import com.barclays.uscb.productcatalogservice.mapper.ProductcatalogMapper;
import com.barclays.uscb.productcatalogservice.model.ProductcatalogHealthResponse;
import com.barclays.uscb.productcatalogservice.repository.ProductcatalogRepository;
import com.barclays.uscb.productcatalogservice.service.ProductcatalogService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class ProductcatalogServiceImpl implements ProductcatalogService {

    private final ProductcatalogRepository productcatalogRepository;

    public ProductcatalogServiceImpl(ProductcatalogRepository productcatalogRepository) {
        this.productcatalogRepository = productcatalogRepository;
    }

    @Override
    public ProductcatalogHealthResponse health() {
        return ApiClient.healthResponse("UP");
    }

    @Override
    public List<Map<String, Object>> getInventory() {
        return productcatalogRepository
                .findAll()
                .stream()
                .map(ProductcatalogMapper::toMap)
                .collect(Collectors.toList());
    }

    @Override
    public List<Map<String, Object>> getProducts() {
        // TODO implement lookup using downstream client for table products
        return Collections.emptyList();
    }
}
