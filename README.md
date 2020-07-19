# python-gitlab
python-gitlab api 

Assumptions:
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
    Choose the desired scopes.
    Click the Create personal access token button.
    Save the personal access token somewhere safe. Once you leave or refresh the page, you won’t be able to access it again.

Configure aws profile for creating secret in secrets manager

  ![picture](img/awscli_profile.png)

