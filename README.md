# python-gitlab
python-gitlab api 

# Assumptions:
- Requires basic python knowledge.
<br />
<br />
- Requires python 3.4+ installed in your machine. I used python 3.8
<br />
<br />
- Install python-gitlab module
<br />
<br />
- sudo pip install - upgrade python-gitlab
<br />
<br />
- Other Python Modules needed
<br />
<br />
  os, sys, urllib3, boto3, ast, yaml, from botocore.exceptions import ClientError
<br />
<br />
- You need to have awscli installed in your machine. You can see this documentation on how to install aws cli
<br />
<br />
  https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
<br />
<br />
- GitLab EE/CE installed and configured and you have admin access
<br />
<br />
- You have AWS account setup and have proper IAM permissions to create secret in AWS Secrets Manager
<br />
<br />

# Create gitlab personal access token:
<br />
- Log in to GitLab.
<br />
<br />
- In the upper-right corner, click your avatar and select Settings.
<br />
<br />
- On the User Settings menu, select Access Tokens.
<br />
<br />
- Choose a name and optional expiry date for the token.
<br />
<br />
- Choose the desired scopes, Here in this case choose "api". 
<br />
<br />
  apiGrants complete read/write access to the API, including all groups and projects, the container registry, and the package registry.
<br />
<br />
- Click the Create personal access token button.
<br />
<br />
- Save the personal access token somewhere safe. Once you leave or refresh the page, you won't be able to access it again.
<br />
<br /> 

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
<br />
- Get the "gitlab-api" key from AWS Secrets Manager
<br />
<br />
- Create a Root Group, if not exists already, of type "internal" and Default Branch Protection enabled
<br />
<br />
- Create a Sub Group , if not exists already, of type "internal"
<br />
<br />
- Assign Owners to the Root Group, if the user is not already Owner
<br />
<br />
- Create a project from an instance template(if EE), within the Sub Group, if not exists already, and enable deploy key on the project(for integrating with any CI like Jenkins)
<br />
<br />
- If you want to create a project from template, In the create_project function, uncomment below attributes and have proper template_project_id value specified in parameters.yaml file
<br />

        # 'use_custom_template': 'true',
        # 'template_project_id': TEMPLATE_PROJ_ID_SPRING
<br />
<br />  
- If you want to enable deploy key on the project, In the create_project function, uncomment below and specify proper Deploy key ID in parameters.yaml file

        # project.keys.enable(JENKINS_DEPLOY_KEY_ID)

<br />
<br />

# Here is the complete script. 
    python-gitlab.py
