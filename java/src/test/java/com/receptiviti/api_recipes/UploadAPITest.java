package com.receptiviti.api_recipes;

import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.multipart.FilePart;
import org.apache.commons.httpclient.methods.multipart.MultipartRequestEntity;
import org.apache.commons.httpclient.methods.multipart.Part;
import org.apache.commons.httpclient.params.HttpMethodParams;
import org.junit.Assert;
import org.junit.Test;
import org.apache.commons.httpclient.HttpClient;

import java.io.File;
import java.io.IOException;
import java.net.URL;


public class UploadAPITest {
    @Test
    public void uploadCSVFile() throws IOException {
        PostMethod filePost = new PostMethod("https://api.receptiviti.com/api/person/upload");

        filePost.setRequestHeader("X-API-KEY",System.getProperty("API_KEY"));
        filePost.setRequestHeader("X-API-SECRET-KEY",System.getProperty("API_SECRET_KEY"));

        ClassLoader classLoader = getClass().getClassLoader();
        URL resource = classLoader.getResource("com/receptiviti/api_recipes/CSV_Upload_samples.csv");
        File fileToUpload = new File(resource.getFile());

        Part[] parts = {
                new FilePart("file", fileToUpload)
        };

        filePost.setRequestEntity(
                new MultipartRequestEntity(parts,
                        filePost.getParams()));

        HttpClient client = new HttpClient();
        client.getHttpConnectionManager().
                getParams().setConnectionTimeout(5000);
        int status = client.executeMethod(filePost);
        Assert.assertEquals(200, status);
    }
}
