package com.receptiviti.api_recipes;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.junit.Assert;
import org.junit.Test;

import java.io.IOException;
import java.lang.reflect.Array;
import java.text.MessageFormat;
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
        HashMap<String, Object> writingSample = getWritingSample();
        person.put("writing_sample", writingSample);

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
        Assert.assertEquals(200, status);

        HashMap<String, Object> responseJson = TestUtils.parseResponseBody(postRequest);
        Assert.assertEquals(person.get("client_reference_id"), responseJson.get("client_reference_id"));

        ArrayList samples = (ArrayList) responseJson.get("writing_samples");
        HashMap<String, Object> analysisResults = (HashMap<String, Object>) samples.get(0);
        Assert.assertEquals(writingSample.get("client_reference_id"), analysisResults.get("client_reference_id"));
        Assert.assertNotNull(analysisResults.get("receptiviti_scores"));
        Assert.assertNotNull(analysisResults.get("liwc_scores"));

    }

    @Test
    public void createPersonOnly() throws IOException {
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
        Assert.assertEquals(200, status);
        HashMap<String, Object> responseJson = TestUtils.parseResponseBody(postRequest);
        Assert.assertEquals(person.get("client_reference_id"), responseJson.get("client_reference_id"));

        ArrayList samples = (ArrayList) responseJson.get("writing_samples");
        Assert.assertEquals(0, samples.size());

    }

    @Test
    public void addSampleForAnExistingPerson() throws IOException {
        ArrayList<HashMap<String, Object>> allPeople = getAllPeople();
        HashMap<String, Object> person = allPeople.get(0);
        String personId = (String) person.get("_id");



        PostMethod postRequest = new PostMethod(getPersonWritingSampleAPIUrl(personId));
        TestUtils.setAuthenticationHeaders(postRequest);

        HashMap<String, Object> writingSample = getWritingSample();

        String responseJsonString = new ObjectMapper().writeValueAsString(writingSample);

        StringRequestEntity requestEntity = new StringRequestEntity(
                responseJsonString,
                "application/json",
                "UTF-8");
        postRequest.setRequestEntity(requestEntity);

        HttpClient client = new HttpClient();
        client.getHttpConnectionManager().
                getParams().setConnectionTimeout(5000);
        int status = client.executeMethod(postRequest);
        Assert.assertEquals(200, status);

        HashMap<String, Object> responseJson = TestUtils.parseResponseBody(postRequest);
        Assert.assertEquals(writingSample.get("client_reference_id"), responseJson.get("client_reference_id"));

        Assert.assertNotNull(responseJson.get("receptiviti_scores"));
        Assert.assertNotNull(responseJson.get("liwc_scores"));
    }


    @Test
    public void getAllPeopleInTheSystem() throws IOException {
        ArrayList people = getAllPeople();
        Assert.assertTrue(people.size()>0);
    }


    public ArrayList<HashMap<String, Object>> getAllPeople() throws IOException {
        GetMethod getRequest = new GetMethod(getPersonAPIUrl());
        TestUtils.setAuthenticationHeaders(getRequest);

        HttpClient client = new HttpClient();
        client.getHttpConnectionManager().
                getParams().setConnectionTimeout(5000);
        int status = client.executeMethod(getRequest);
        Assert.assertEquals(200, status);
        return TestUtils.parseResponseBody(getRequest);
    }

    public String getPersonAPIUrl() {
        return MessageFormat.format("{0}/api/person", TestUtils.getBaseUrl());
    }

    public String getPersonWritingSampleAPIUrl(String personId) {
        return MessageFormat.format("{0}/{1}/writing_samples", getPersonAPIUrl(),personId);
    }

    private HashMap<String, Object> createPerson() {
        HashMap<String, Object> person = new HashMap<String, Object>();
        person.put("gender",1);
        person.put("client_reference_id", UUID.randomUUID().toString());
        person.put("name",UUID.randomUUID().toString());
        person.put("tags",new String[]{"tag1", "tag2"});
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
