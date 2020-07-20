# python-gitlab
python-gitlab api 

Use case:
Create a Root Group, if not exists already, of type "internal" and Default Branch Protection enabled
Create a Sub Group , if not exists already, of type "internal"
Assign Owner to the Root Group, if the user is not already Owner.
Create a project within the Sub Group, if not exists already, and enable deploy key on the project


Assumptions:
<br />
Requires basic python knowledge.
<br />
You need to have awscli installed in your machine. You can see this documentation on how to install aws cli
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
<br />


Create gitlab personal access token
https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html

You can create as many personal access tokens as you like from your GitLab profile.

    Log in to GitLab.
    In the upper-right corner, click your avatar and select Settings.
    On the User Settings menu, select Access Tokens.
    Choose a name and optional expiry date for the token.
    Choose the desired scopes, Here in this case choose api.
    Click the Create personal access token button.
    Save the personal access token somewhere safe. Once you leave or refresh the page, you won’t be able to access it again.

Configure aws profile for creating secret in secrets manager

  ![picture](img/awscli_profile.png)

Create secret in AWS Secrets Manager
<br />
  The contents of the file mycreds.json
  <br />  
  {"gitlab-api": "yourAPIKey"}
<br />  

  ![picture](img/secretsmanager.png)

  Example Output:
  {
  "ARN": "arn:aws:secretsmanager:us-east-1:123456789012: secret:gitlab-api-a1b2c3",
  "Name": "gitlab-api",
  "VersionId": "EXAMPLE1-90ab-cdef-fedc-ba987EXAMPLE"
  }

<br />  







A comprehensive guide leveraging python-gitlab api to automate creation of groups, sub groups, projects, assign owners to a group

Assumptions:
Requires basic python knowledge.
<br />
Requires python 3.4+ installed in your machine. I used python 3.8
<br />
Install python-gitlab module
<br />
sudo pip install - upgrade python-gitlab
<br />
Other Python Modules needed
<br />
os, sys, urllib3, boto3, ast, yaml, from botocore.exceptions import ClientError


You need to have awscli installed in your machine. You can see this documentation on how to install aws cli.

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
GitLab EE/CE installed and configured and you have admin access.
You have AWS account setup and have proper IAM permissions to create secret in AWS Secrets Manager.

    Create gitlab personal access token:
    Log in to GitLab.
    In the upper-right corner, click your avatar and select Settings.
    On the User Settings menu, select Access Tokens.
    Choose a name and optional expiry date for the token.
    Choose the desired scopes, Here in this case choose "api". 
    apiGrants complete read/write access to the API, including all groups and projects, the container registry, and the package registry.
    Click the Create personal access token button.
    Save the personal access token somewhere safe. Once you leave or refresh the page, you won't be able to access it again.
