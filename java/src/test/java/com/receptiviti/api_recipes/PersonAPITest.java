package com.receptiviti.api_recipes;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.apache.commons.httpclient.methods.multipart.FilePart;
import org.apache.commons.httpclient.methods.multipart.MultipartRequestEntity;
import org.apache.commons.httpclient.methods.multipart.Part;
import org.apache.http.entity.StringEntity;
import org.junit.Assert;
import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.UUID;

public class PersonAPITest {

    @Test
    public void createPersonWithWritingSampleRequest() throws IOException {
        PostMethod postRequest = new PostMethod("https://api.receptiviti.com/api/person");
        postRequest.setRequestHeader("X-API-KEY",System.getProperty("API_KEY"));
        postRequest.setRequestHeader("X-API-SECRET-KEY",System.getProperty("API_SECRET_KEY"));

        HashMap<String, Object> person = createPerson();



        String responseJsonString = new ObjectMapper().writeValueAsString(person);

        StringRequestEntity requestEntity = new StringRequestEntity(
                responseJsonString,
                "application/json",
                "UTF-8");
        postRequest.setRequestEntity(requestEntity);

        HttpClient client = new HttpClient();
        client.getHttpConnectionManager().
                getParams().setConnectionTimeout(5000);
        int status = client.executeMethod(postRequest);
        System.out.println(postRequest.getResponseBodyAsString());
        Assert.assertEquals(200, status);

    }

    private HashMap<String, Object> createPerson() {
        HashMap<String, Object> person = new HashMap<String, Object>();
        person.put("gender",1);
        person.put("client_reference_id", UUID.randomUUID().toString());
        person.put("name",UUID.randomUUID().toString());
        person.put("tags",new String[]{"tag1", "tag2"});
        person.put("writing_sample", getWritingSample());
        return person;
    }

    private HashMap<String, Object> getWritingSample() {
        HashMap<String, Object> writingSample = new HashMap<String, Object>();
        writingSample.put("content", "The tortoises of the genus Gopherus have been clocked at rates of 0.21 to 0.48 km (0.13 to 0.30 miles) per hour.") ;
        writingSample.put("content_source", 0) ;
        writingSample.put("tags", new String[]{"tag1", "tag2"}) ;
        writingSample.put("sample_date", ZonedDateTime.now().format(DateTimeFormatter.ISO_INSTANT)) ;
        writingSample.put("language", "english") ;
        writingSample.put("client_reference_id", UUID.randomUUID().toString()) ;
        return writingSample;
    }
}
