package com.divanv.muninn.repositories;

import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface ChatLogRepository extends CrudRepository<HistoryEntry, Long> {
    List<HistoryEntry> findByUserId(Long userId);
}
