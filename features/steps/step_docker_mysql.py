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
    response = context.client.pull(repository,tag)
    print (response)
    assert "Status: Image is up to date" in response

@then('docker version is >={ver}')
def step_impl(context,ver):
    assert context.client.version()["Version"] >= ver

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False

