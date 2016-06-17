#Calculating an LSM score

Language Style Matching (LSM) is a score that indicate the extent to which 2 people's conversation with each other is in sync.

##Process

###Add content consisting of conversation between the 2 people
  - create both people (if they do not exist)

  ```POST /api/person```

  - add each item of content spoken by person 1 to person 2 against person 1 with person 2 as the recipient, and vice versa

  ```POST /api/person/<person id>/contents```

  - request the LSM score

  ```GET /api/lsm_score?person1=<person1 id>&person2=<person2 id>```

The sample code encapsulates these steps into the following process:-

Extract the content into 2 files, one for each person. Name the file for the speaker. Call the sample code and pass the names of the 2 files.

```
$ python lsm.py <api key> <api secret> <file1> <file2>
score: ##
```
