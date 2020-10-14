import os
import logging
import datetime
import shutil
from time import sleep
from appium import webdriver
from allure_commons._allure import attach
from allure_commons.types import AttachmentType

from capabilities.ios_caps import ios_caps
from capabilities.android_caps import android_caps
from utilities.jira import jira
from behave.model_core import Status


def before_all(context):
    #jira.connect_to_jira()
    pass

def before_feature(context, feature):

    context.driver = None

    if 'iOS' in feature.tags:
        context.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4724/wd/hub',
            desired_capabilities=ios_caps)

    elif 'android' in feature.tags:
        context.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=android_caps)



def after_feature(context, feature):
    context.driver.quit()


def before_scenario(context, scenario):
    logging.info("START scenario: " + scenario.name)

def after_step(context, step):

    if step.status == "failed":
        attach(context.driver.get_screenshot_as_png(), name=datetime.datetime.now().timestamp(), attachment_type = AttachmentType.PNG)



def after_scenario(context, scenario):
    logging.info(scenario.status)
    if scenario.status == Status.failed:

        scenario_name = "Scenario Name: " + scenario.name
        description = ""
        for step in scenario.steps:
            rows = ""
            description += str(step) + "\n"
            if step.table is not None:
                rows = '\n'.join(str(row) for row in step.table.rows)
                rows = rows.replace("Row [", "")
                rows = rows.replace("]", "")
                description += str(rows) + "\n"
        description = description.replace("<", "")
        description = description.replace(">", "")
        description += str(datetime.datetime.now()) + "\n"

        #new_issue = jira.add_issue(scenario_name, description)
        #jira.attach_screenshots_in_jira(new_issue, capture_screenshots_for_jira(context))


    logging.info("FINISHED scenario: " + scenario.name)


def capture_screenshots_for_jira(context):
    path = os.getcwd()+"/temp"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    path_to_capture_screenshot = path+"/"+str(datetime.datetime.now().timestamp())+".png"
    context.driver.get_screenshot_as_file(path_to_capture_screenshot)
    return path_to_capture_screenshot