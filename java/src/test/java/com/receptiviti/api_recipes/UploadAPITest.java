package com.receptiviti.api_recipes;

import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.multipart.FilePart;
import org.apache.commons.httpclient.methods.multipart.MultipartRequestEntity;
import org.apache.commons.httpclient.methods.multipart.Part;
import org.junit.Assert;
import org.junit.Test;
import org.apache.commons.httpclient.HttpClient;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;


public class UploadAPITest {
    @Test
    public void uploadCSVFile() throws IOException, InterruptedException {

        PostMethod filePost = new PostMethod(getPersonUploadAPIUrl());

        TestUtils.setAuthenticationHeaders(filePost);

        File fileToUpload = getFileToUpload();

        Part[] parts = {
                new FilePart("file", fileToUpload)
        };

        filePost.setRequestEntity( new MultipartRequestEntity(parts, filePost.getParams()));

        HttpClient client = new HttpClient();
        client.getHttpConnectionManager().
                getParams().setConnectionTimeout(5000);
        int status = client.executeMethod(filePost);
        Assert.assertEquals(200, status);
        HashMap<String, Object> latestResponse = TestUtils.parseResponseBody(filePost);

        //Pinging for status
        String statusUrl = getStatusUrl(latestResponse);
        GetMethod uploadRequest = new GetMethod(statusUrl);
        TestUtils.setAuthenticationHeaders(uploadRequest);

        int idx = 1;
        while (!isDone(latestResponse)){
            Thread.sleep(5000);
            int new_status_code = client.executeMethod(uploadRequest);
            Assert.assertEquals(200, new_status_code);
            latestResponse = TestUtils.parseResponseBody(uploadRequest);
            System.out.format("Retry %d: Status- %s, Last Updated - %s", idx, latestResponse.get("status"), latestResponse.get("updated"));
            System.out.println();
            idx++;

        }
        Assert.assertEquals(5, getResult(latestResponse).get("success"));

    }

    private HashMap<String, Object> getResult(HashMap<String, Object> latestResponse) {
        return (HashMap<String, Object>) latestResponse.get("result");
    }

    public String getStatusUrl(HashMap<String, Object> uploadResponse) {
        String statusUrlPart = (String) ((HashMap<String, Object>) ((HashMap<String, Object>) uploadResponse.get("_links")).get("self"))
                .get("href");
        return TestUtils.getBaseUrl()+statusUrlPart;
    }

    public String getPersonUploadAPIUrl() {
        return TestUtils.getBaseUrl() + "/api/person/upload";
    }

    private File getFileToUpload() {
        ClassLoader classLoader = getClass().getClassLoader();
        URL resource = classLoader.getResource("com/receptiviti/api_recipes/CSV_Upload_samples.csv");
        return new File(resource.getFile());
    }

    private boolean isDone(HashMap<String, Object> uploadResponse){
        String status = (String) uploadResponse.get("status");
        List<String> terminalStatuses = Arrays.asList("completed", "failed", "errored");
        return terminalStatuses.contains(status);
    }

}
