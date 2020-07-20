#!/usr/bin/env python3
#This is an automation script for onboarding teams to GitLab
#Created by: Balaram Patibandla
#
#Installation:
#    #sudo pip install --upgrade python-gitlab
#
#Use case:
#Assuming gitlap api key is created and stored in AWS Secrets Manager with secret_name "gitlab-api"
#Create a Root Group, if not exists already, of type "internal" and Default Branch Protection enabled
#Create a Sub Group , if not exists already, of type "internal"
#Assign Owners to the Root Group, if the user is not already Owner.
#Create a project from an instance template(if EE), within the Sub Group, if not exists already, and enable deploy key on the project
#    #If you want to create a project from tekplate, In the create_project function, uncomment below attributes and have proper  Template proj ID specified in parameters.yaml file
#        # 'use_custom_template': 'true',
#        # 'template_project_id': TEMPLATE_PROJ_ID_SPRING
#    #If you want to enable deploy key on the project, In the create_project function, uncomment below and specify proper Deploy key ID in parameters.yaml file
#        # project.keys.enable(JENKINS_DEPLOY_KEY_ID)
#################################################################
import gitlab
import os
import sys
import urllib3
import boto3
from botocore.exceptions import ClientError
import ast
import yaml

"""
Disable ssl warning
Returns:
    this code suppresses ssl warning, for disabling certificate check
"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parameters_file = open(os.path.join(sys.path[0], "parameters.yaml"), "r")
parsed_yaml_file = yaml.load(parameters_file, Loader=yaml.FullLoader)
print(parsed_yaml_file["parameters_dictionary"])

#set the env variables
os.environ["GITLAB_SERVER"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_SERVER')
os.environ["GITLAB_ROOTGROUP"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_ROOTGROUP')
os.environ["GITLAB_SUBGROUP"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_SUBGROUP')
os.environ["GITLAB_PROJECT"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_PROJECT')
os.environ["GITLAB_ROOT_DESCRIPTION"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_ROOT_DESCRIPTION')
os.environ["GITLAB_SUB_DESCRIPTION"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_SUB_DESCRIPTION')
os.environ["GITLAB_GROUP_OWNER"] = parsed_yaml_file["parameters_dictionary"].get('GITLAB_GROUP_OWNER')
os.environ["JENKINS_DEPLOY_KEY_ID"] = parsed_yaml_file["parameters_dictionary"].get('JENKINS_DEPLOY_KEY_ID')
os.environ["TEMPLATE_PROJ_ID_SPRING"] = parsed_yaml_file["parameters_dictionary"].get('TEMPLATE_PROJ_ID_SPRING')

#get the env variables
GITLAB_SERVER = os.getenv("GITLAB_SERVER")
GITLAB_ROOTGROUP = os.getenv("GITLAB_ROOTGROUP")
GITLAB_SUBGROUP = os.getenv("GITLAB_SUBGROUP")
GITLAB_PROJECT = os.getenv("GITLAB_PROJECT")
GITLAB_ROOT_DESCRIPTION = os.getenv("GITLAB_ROOT_DESCRIPTION")
GITLAB_SUB_DESCRIPTION = os.getenv("GITLAB_SUB_DESCRIPTION")
GITLAB_GROUP_OWNER = os.getenv("GITLAB_GROUP_OWNER")
JENKINS_DEPLOY_KEY_ID = os.getenv("JENKINS_DEPLOY_KEY_ID")
TEMPLATE_PROJ_ID_SPRING = os.getenv("TEMPLATE_PROJ_ID_SPRING")


def get_secret():
    secret_name = "gitlab-api"
    region_name = "us-east-1"

    session = boto3.session.Session(profile_name='balaram')
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        #We get Dictionary
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            print(type(get_secret_value_response))
            print(get_secret_value_response)
            text_secret_data = get_secret_value_response['SecretString']
            print("Here is the value:", text_secret_data)
            #Convert string text_secret_data to dictionary
            text_secret_data_value = ast.literal_eval(text_secret_data).get(secret_name)
            # print("text_secret_data_value : ", text_secret_data_value)
            return text_secret_data_value
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            print(binary_secret_data)

#Create gl object to authenticate to gitlab environment
GITLAB_TOKEN = get_secret()
print("Here is the token GITLAB_TOKEN:", GITLAB_TOKEN)
gl = gitlab.Gitlab(GITLAB_SERVER, private_token=GITLAB_TOKEN, ssl_verify=False, api_version="4")
gl.auth()

class gitlab_onboarding():
    ##########Create Root Group########    
    def create_root_group(self):
        global group
        group_list = gl.groups.list(as_list=False)
        group_name = []
        group_id = []
        for group in group_list:
            """
            for each group in group_list, get the name attribute and append to group_name list
            """
            group_name.append(group.attributes.get('name'))
            group_id.append(group.attributes.get('id'))
        print("Here is the list of groups with group_name: ", group_name)
        print("Here is the list of groups with group_id: ", group_id)

        #Converting these 2 lists group_name, group_id into dictionary
        self.group_name_id = dict(zip(group_name, group_id))
        print("Name and id map of groups", self.group_name_id)
        if GITLAB_ROOTGROUP in group_name:
            print("The GITLAB_ROOTGROUP exists already")
            print("Here is the group_name: ", GITLAB_ROOTGROUP)
            print("Here is the group_id: ", self.group_name_id.get(GITLAB_ROOTGROUP))
            group = self.group_name_id.get(GITLAB_ROOTGROUP)
            print("checking variable group:", type(group))
            return group

        else:
            print("The GITLAB_ROOTGROUP does not exist and we are going to creating it")
            self.rootGroup = gl.groups.create({
                'name': GITLAB_ROOTGROUP,
                'path': GITLAB_ROOTGROUP,
                'visibility': 'internal',
                'lfs_enabled': 'true',
                'description': GITLAB_ROOT_DESCRIPTION,
                'default_branch_protection': '2'
                })
            print("This is the rootGroup : ", self.rootGroup)
            self.rootGroup.save()
            group = gl.groups.get(self.rootGroup.attributes.get('id'))
            return group
    ########Create Sub Group###############
    def create_sub_group(self):
        global subgroup
        group = gl.groups.get(GITLAB_ROOTGROUP)
        print("CHECKING:", group)
        subgroups = group.subgroups.list()
        print(f"Here is the list of sub groups for the root group {GITLAB_ROOTGROUP}", subgroups)
        print ("check the data type :", type(subgroups))
        sub_group_name = []
        sub_group_id = []
        for sub_group in subgroups:
            sub_group_name.append(sub_group.attributes.get('name'))
            sub_group_id.append(sub_group.attributes.get('id'))
        print("Here is the list of sub groups with sub_group_name: ", sub_group_name)
        print("Here is the list of sub groups with sub_group_id: ", sub_group_id)
        #Converting these 2 lists sub_group_name, sub_group_id into dictionary
        self.sub_group_name_id = dict(zip(sub_group_name, sub_group_id))
        print("Name and id map of subgroups", self.sub_group_name_id)
        if GITLAB_SUBGROUP not in sub_group_name:
            self.subGroup = gl.groups.create({
                'name': GITLAB_SUBGROUP,
                'path': GITLAB_SUBGROUP,
                'visibility': 'internal',
                'description': GITLAB_SUB_DESCRIPTION,
                'parent_id': group.attributes.get('id')
                })
            print("This is the subGroup : ", self.subGroup)
            self.subGroup.save()
            subgroup = gl.groups.get(self.subGroup.attributes.get('id'))
            print("checking variable subgroup:", subgroup)
            return subgroup

        else:
            print("The GITLAB_SUBGROUP exists already")
            print("Here is the sub_group_name: ", GITLAB_SUBGROUP)
            subgroup = self.sub_group_name_id.get(GITLAB_SUBGROUP)
            print("checking variable group:", subgroup)
            return subgroup

    ########Assign Members to Root Group#######
    def assign_members(self):
        """
        Assign Owner for the root group
        https://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html#group-members
        gitlab.GUEST_ACCESS = 10
        gitlab.REPORTER_ACCESS = 20
        gitlab.DEVELOPER_ACCESS = 30
        gitlab.MAINTAINER_ACCESS = 40
        gitlab.OWNER_ACCESS = 50
        """
        group = gl.groups.get(GITLAB_ROOTGROUP)
        print(type(GITLAB_GROUP_OWNER))
        print("Here is the string : ", GITLAB_GROUP_OWNER)
        print("Here is the list : ", GITLAB_GROUP_OWNER.strip("][").split(", "))
        print(type(GITLAB_GROUP_OWNER.strip('][').split(", ")))
        GITLAB_GROUP_OWNER_LIST = GITLAB_GROUP_OWNER.strip('][').split(", ")
        print("Here is the GITLAB_GROUP_OWNER_LIST : ", GITLAB_GROUP_OWNER.strip("][").split(", "))
        print("Here is the group members list of id: ", group.members.list())

        members = group.members.list()
        member_id = []
        for member in members:
            print(member.attributes.get('username'))
            member_id.append(member.attributes.get('id'))
        print("list of member_id on the group: ", member_id)

        for owner in GITLAB_GROUP_OWNER_LIST:
            try:
                user = gl.users.list(username=owner)[0]
                user_id = user.attributes.get('id')
                print("the user_id,username is : ", user_id, owner)

                if user_id not in member_id:
                    member = group.members.create({'user_id': user_id,
                                                'access_level': gitlab.OWNER_ACCESS})
                    member.save()
                    print("trying to print member: ", member)
                else:
                    print(f"{owner} is already GROUP_OWNER, Hence not assigning as Owner", "\n")
            except IndexError:
                user = 'null'
                print(f"""
{owner} is not in gitlab yet,so either have to create the {owner} or
if {owner} is already created, {owner} has to login to gitlab atleast once
                    """)

    #######Create a Project##################
    def create_project(self):
        global project
        projects = gl.projects.list(search=GITLAB_PROJECT)
        print(projects)
        project_name = []
        project_id = []
        for project in projects:
            project_name.append(project.attributes.get('name'))
            project_id.append(project.attributes.get('id'))
        print("Here is the list of project with project_name: ", project_name)
        print("Here is the list of sub groups with project_id: ", project_id)
        #Converting these 2 lists project_name, project_id into dictionary
        self.project_name_id = dict(zip(project_name, project_id))
        print("Name and id map of subgroups", self.project_name_id)
        if GITLAB_PROJECT in project_name:
            print("The GITLAB_PROJECT exists already")
            print("Here is the project_name: ", GITLAB_PROJECT)
            project = self.project_name_id.get(GITLAB_PROJECT)
            print("checking variable project:", project)
            return project
        else:
            group_id = gl.groups.list(search=GITLAB_SUBGROUP)[0].id
            project = gl.projects.create({
                'name': GITLAB_PROJECT,
                'namespace_id': group_id,
                'auto_devops_enabled': 'false',
                'visibility': 'internal',
                # 'use_custom_template': 'true',
                # 'template_project_id': TEMPLATE_PROJ_ID_SPRING
                })
            #Enable deploy key on the project
            """
            project.keys.enable(key_id)
            """
            # project.keys.enable(JENKINS_DEPLOY_KEY_ID)
            project.save()
            print(f"Here is the create project under {GITLAB_SUBGROUP}", project)
            return project


if __name__ == "__main__":
    onboarding = gitlab_onboarding()
    onboarding.create_root_group()
    onboarding.assign_members()
    onboarding.create_sub_group()
    onboarding.create_project()