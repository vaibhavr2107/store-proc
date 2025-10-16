package com.barclays.uscb.suppliermanagementservice.service;

import java.util.List;
import java.util.Map;

import com.barclays.uscb.suppliermanagementservice.model.SuppliermanagementHealthResponse;

public interface SuppliermanagementService {

    SuppliermanagementHealthResponse health();

    List<Map<String, Object>> getSuppliers();
}
