package com.barclays.uscb.userservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.barclays.uscb.userservice.entity.UserEntity;

public interface UserRepository extends JpaRepository<UserEntity, String> {
}
