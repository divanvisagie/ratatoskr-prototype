package com.divanv.muninn.repositories;


import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;
@Data
@Document (collection = "user")
public class User {

    @Id
    public String id;

    public String telegramUsername;

    public Integer accessLevel;

    @CreatedDate
    public Date createdAt;

    @LastModifiedDate
    public Date updatedAt;

}
