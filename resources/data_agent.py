import os
import logging
import json
import requests
from flask_restful import Resource
from flask_restful import request
from common import push_event

logger = logging.getLogger('data_cache')
RULE_HANDLER_URL = os.environ.get('RULE_HANDLER_URL', 'http://127.0.0.1:5000/rulehandler')

class Issue(Resource):
    def post(self):
        logger.debug(json.dumps(request.json, indent=4))
        #  TODO This won't work, the rule handler will parse
        #  it into an empty string, find out why
        #  res = requests.post(RULE_HANDLER_URL, json=json.dumps(request.json, indent=4))
        res = requests.post(RULE_HANDLER_URL, json=request.json)
        if res.status_code >= 300:
            logger.error(f'error status_code: {res.status_code}, content: {res.text}')
            return "Internal Error", 500
        rule_json = res.json()[0] # TODO Is the rule object a list or dict?
        logger.debug(json.dumps(rule_json, indent=4))
        #  TODO Construct the Event Object with rule and issue info
        rule_type = rule_json['ruleType']
        target_info = rule_json['infoPayload'] if rule_type == 'info' else ""
        target_label = "" # TODO Where to get the value?
        target_assignee_id = "" # TODO Where to get the value?

        event_obj = {
            'issueID': rule_json['issueID'],
            'eventType': rule_json['ruleType'],
            'targetInfo': target_info,
            'targetLabel': target_label,
            'targetAssigneeID': target_assignee_id,
            'pushTime': rule_json['exeTime'],
        }

        # TODO Get delay by comparing the current time and event_obj.pushTime
        push_event(json.dumps(event_obj), delay=2000)
        return "", 200

    def get(self):
        pass
