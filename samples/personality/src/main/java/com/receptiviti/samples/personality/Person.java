package com.receptiviti.samples.personality;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Person {
    @JsonIgnore
    String id;

    @JsonProperty(value="name")
    String name;

    @JsonProperty(value="person_handle")
    String handle;

    @JsonProperty(value="gender")
    Integer gender;

    public Person(String name, String handle, Integer gender) {
        this.id = null;
        this.name = name;
        this.handle = handle;
        this.gender = gender;
    }

    public Person(Person person) {
        this.id = person.id;
        this.name = person.name;
        this.handle = person.handle;
        this.gender = person.gender;
    }
}
