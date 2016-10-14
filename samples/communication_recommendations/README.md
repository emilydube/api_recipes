#Communication Recommendations

The Receptiviti API provides you an easy way to learn how to communicate with a person based on their personality. The person's personality itself is assessed based on natural language content i.e words spoken, written or typed by that person. 


##Process

###Create a person in the system

  - create a person in the system

  ```POST /api/person```

###Add some content

  - add each item of content spoken/written by that person

  ```POST /api/person/<person id>/contents```

###Get the communication recommendation

  - get the communication recommendation from the profile of that person
  
  ```GET /api/person/<person id>/profile```
    In the response, the key "communication_recommendations" will have the necessary information

## Running the sample code

### Pre-requisite

  - python 2.7
  - git
  - Registered account with Receptiviti API with a a valid API Key and Secret Key. 

### Installation

  - Check out this repository on your machine
  - Change directory on the command line to $GIT_ROOT/samples/communication_recommendations
  - Install dependencies
  
     ```pip install -r requirements.txt```
  
### Data
  - Capture each independent content sample in a seperate text file (.txt extension) and drop it into $REPO_ROOT/samples/content folder
  
### Running the sample

```
$ python get_cr.py --key <api key> --secret <api secret> --name <person_name>
Recommendations: ##
```
