#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Based on ``behave tutorial``
"""

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
from behave import given, when, then
import docker

def filter_unicode_data(obj):
    if type(obj) in (int, float, str, bool):
        return obj
    elif type(obj) == unicode:
        return str(obj)
    elif type(obj) in (list, tuple, set):
        obj = list(obj)
        for i,v in enumerate(obj):
            obj[i] = filter_unicode_data(v)
    elif type(obj) == dict:
        obj_str = {}
        for i,v in obj.items():
            obj_str[filter_unicode_data(i)] = filter_unicode_data(v)
        return obj_str
    return obj

#
#  Docker
#

DEFAULT_BASE_URL = 'unix://var/run/docker.sock'
EXEC_DRIVER_IS_NATIVE = True

@when('we connect to docker')
def step_impl(context):
    context.client = docker.Client(base_url=DEFAULT_BASE_URL, timeout=5)
    assert not (context.client is None)

@when("we create an image {tag} based on {path}")
def step_impl(context,tag,path):
    response = context.client.build(path,tag)
    assert "Success" in response

@when("we pull an image {repository}:{tag}")
def step_impl(context,repository,tag):
    response =context.client.pull(repository,tag)
    print (response)
    assert "Status: Image is up to date" in response

@when("we create container {tag} from image {repository}")
def step_impl(context,repository,tag):
    cont = "/"+ tag
    response = filter_unicode_data(context.client.containers(all=True))
    for i in range(0,len(response)):
        print (response[i])
        if cont in response[i]['Names'] :
            if "Up" in response[i]['Status'] :
                context.client.stop(container=tag)
            context.client.remove_container(container=cont)
    response = filter_unicode_data(context.client.create_container(image=repository,name=tag))
    print (response)
    print ()
    assert response["Warnings"] is None

@when("we start container {tag}")
def step_impl(context,tag):
    response = context.client.start(container=tag)
    print (response)
    print (response)
    print ()
    assert response is None

@Then("we can see {tag} in the running containers list")
def step_impl(context,tag):
    cont = "/"+ tag
    response = filter_unicode_data(context.client.containers(all=False))
    for i in range(0,len(response)):
        print (response[i])
        if cont in response[i]['Names'] :
            if "Up" in response[i]['Status'] :
                pass
                return
    assert False

@then("we can see {image} in the image list")
def step_impl(context,image):
    response = context.client.images(name=image)[0]
    response = filter_unicode_data(response)
    print(response)
    print()
    assert image in response["RepoTags"][0]

@then('docker version is >={ver}')
def step_impl(context,ver):
    assert context.client.version()["Version"] >= ver

#
# Behave
#

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False
