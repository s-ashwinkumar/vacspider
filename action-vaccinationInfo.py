#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import io
import sys

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import requests

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """

    :param hermes:
    :param intentMessage:
    :param conf:
    :return:
    """
    if len(intentMessage.slots.disease_indicator) > 0:
        disease = intentMessage.slots.disease_indicator.first().value
        try:
            URL = 'https://oshaw-vacspider-backend.herokuapp.com/api/diseases'
            PARAMS = {'name':disease}
            response = requests.get(url = URL, params = PARAMS)
            result = response.text.encode('ascii')
            hermes.publish_end_session(intentMessage.session_id, "I want to test this if this works")
        except:
            print "Unexpected error:", sys.exc_info()[0]
            hermes.publish_end_session(intentMessage.session_id, "An error occured")
    else:
        hermes.publish_end_session(intentMessage.session_id, "An error occured")



if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("ashwin24:vaccinationInfo", subscribe_intent_callback) \
         .start()
