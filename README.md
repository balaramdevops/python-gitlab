# python-gitlab
python-gitlab api 

# Assumptions:
<br />
- Requires basic python knowledge.
<br />
<br />
- Requires python 3.4+ installed in your machine. I used python 3.8
<br />
- Install python-gitlab module
<br />
- sudo pip install - upgrade python-gitlab
<br />
- Other Python Modules needed
<br />
  os, sys, urllib3, boto3, ast, yaml, from botocore.exceptions import ClientError
<br />
- You need to have awscli installed in your machine. You can see this documentation on how to install aws cli
<br />
  https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
<br />
- GitLab EE/CE installed and configured and you have admin access
<br />
- You have AWS account setup and have proper IAM permissions to create secret in AWS Secrets Manager
<br />
# Create gitlab personal access token:
<br />
- Log in to GitLab.
<br />
- In the upper-right corner, click your avatar and select Settings.
<br />
- On the User Settings menu, select Access Tokens.
<br /><br />
- Choose a name and optional expiry date for the token.
<br />
- Choose the desired scopes, Here in this case choose "api". 
<br />
  apiGrants complete read/write access to the API, including all groups and projects, the container registry, and the package registry.
<br />
- Click the Create personal access token button.
<br />
- Save the personal access token somewhere safe. Once you leave or refresh the page, you won't be able to access it again.
    

# Configure aws profile for creating secret in secrets manager

   ![picture](img/awscli_profile.png)


  # Create secret in AWS Secrets Manager
      Make sure the file mycreds.json is in the same location from where you are executing the awscli command.  
      
      The contents of the file mycreds.json
      {"gitlab-api": "yourAPIKey"}

   ![picture](img/secretsmanager.png)

      Example Output:
      {
      "ARN": "arn:aws:secretsmanager:us-east-1:123456789012: secret:gitlab-api-a1b2c3",
      "Name": "gitlab-api",
      "VersionId": "EXAMPLE1-90ab-cdef-fedc-ba987EXAMPLE"
      }



# Use cases of python script:
<br />
- Assuming gitlab api key is created and stored in AWS Secrets Manager with secret_name "gitlab-api"
<br />
- Get the "gitlab-api" key from AWS Secrets Manager
<br />
- Create a Root Group, if not exists already, of type "internal" and Default Branch Protection enabled
<br />
- Create a Sub Group , if not exists already, of type "internal"
<br />
- Assign Owners to the Root Group, if the user is not already Owner
<br />
- Create a project from an instance template(if EE), within the Sub Group, if not exists already, and enable deploy key on the project(for integrating with any CI like Jenkins)
<br />
- If you want to create a project from template, In the create_project function, uncomment below attributes and have proper template_project_id value specified in parameters.yaml file
<br />

        # 'use_custom_template': 'true',
        # 'template_project_id': TEMPLATE_PROJ_ID_SPRING
 <br />  
- If you want to enable deploy key on the project, In the create_project function, uncomment below and specify proper Deploy key ID in parameters.yaml file

        # project.keys.enable(JENKINS_DEPLOY_KEY_ID)


# Here is the complete script. 
    python-gitlab.py
