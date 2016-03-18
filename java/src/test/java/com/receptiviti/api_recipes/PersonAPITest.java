package com.receptiviti.api_recipes;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.junit.Assert;
import org.junit.Test;

import java.io.IOException;
import java.lang.reflect.Array;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;

public class PersonAPITest {

    @Test
    public void createPersonWithWritingSampleRequest() throws IOException {
        PostMethod postRequest = new PostMethod(getPersonAPIUrl());
        TestUtils.setAuthenticationHeaders(postRequest);

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
        HashMap<String, Object> o = TestUtils.parseResponseBody(postRequest);

        ArrayList writing_samples = (ArrayList) o.get("writing_samples");
        HashMap<String, Object> analysisResults = (HashMap<String, Object>) writing_samples.get(0);
        Assert.assertNotNull(analysisResults.get("receptiviti_scores"));
        Assert.assertNotNull(analysisResults.get("liwc_scores"));
        Assert.assertEquals(200, status);

    }

    public String getPersonAPIUrl() {
        return TestUtils.getBaseUrl() + "/api/person";
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
