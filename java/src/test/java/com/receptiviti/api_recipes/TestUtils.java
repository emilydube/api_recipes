package com.receptiviti.api_recipes;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.httpclient.HttpMethod;
import org.apache.commons.httpclient.methods.PostMethod;

import java.io.IOException;
import java.util.HashMap;

public class TestUtils {
    static <T> T parseResponseBody(HttpMethod httpMethod) throws IOException {
        JsonFactory factory = new JsonFactory();
        ObjectMapper mapper = new ObjectMapper(factory);
        TypeReference<T> typeRef
                = new TypeReference<T>() {};

        return mapper.readValue(httpMethod.getResponseBodyAsString(), typeRef);
    }

    static void setAuthenticationHeaders(HttpMethod method) {
        method.setRequestHeader("X-API-KEY",System.getProperty("API_KEY"));
        method.setRequestHeader("X-API-SECRET-KEY",System.getProperty("API_SECRET_KEY"));
    }

    public static String getBaseUrl() {
        String providedBaseUrl = System.getProperty("BASE_URL");
        return providedBaseUrl != null ? providedBaseUrl : "https://api.receptiviti.com";
    }
}
