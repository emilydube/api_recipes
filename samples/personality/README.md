# Sample Java application to extract a Personality Snapshot from the Receptiviti API

##Process

The process to get a personality snapshot from the Receptiviti API is:-

- obtain some content for a person
- submit that content with the person's data

The returned data will contain the snapshot (as well as the raw scores)

##Usage

Once you have built this project you can run it as follows:-

```java -j personality.jar <filename>```

The filename will be used as the person's name and the file contents will be used as the person's writing.
