package com.receptiviti.samples.personality;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Content {
    @JsonIgnore
    public String id;

    @JsonIgnore
    public List<String> snapshot;

    @JsonProperty(value = "content_handle")
    public String name;

    @JsonProperty(value = "language_content")
    public String content;

    @JsonProperty(value = "content_source")
    public Integer source;

    public Content(String filename) {
        this.id = null;
        this.source = 6;
        File contentFile = new File(filename);
        this.name = contentFile.getName().split("\\.")[0];
        try {
            this.content = new String(Files.readAllBytes(Paths.get(filename)));
        } catch (IOException e) {
            System.err.println("Could not read file: " + e.getMessage());
        }
    }

    public Content(Content content) {
        this.id = content.id;
        this.source = content.source;
        this.name = content.name;
        this.content = content.content;
    }
}
