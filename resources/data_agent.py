import os
import logging
import json
import requests
from datetime import datetime
from flask_restful import Resource
from flask_restful import request
from common import push_event

logger = logging.getLogger('data_cache')
RULE_HANDLER_URL = os.environ.get('RULE_HANDLER_URL', 'http://127.0.0.1:5000/rulehandler')
STRATEGY_EXECUTOR_URL = os.environ.get('STRATEGY_EXECUTOR_URL', 'http://127.0.0.1:8002/api/Executor/execute-event/')

class Issue(Resource):
    def post(self):
        logger.debug(json.dumps(request.json, indent=4))
        #  TODO This won't work, the rule handler will parse
        #  it into an empty string, find out why
        #  res = requests.post(RULE_HANDLER_URL, json=json.dumps(request.json, indent=4))

        repoInfo = request.json['repoInfo']

        rule_req_obj = {
            'issueID': request.json['issueID'],
            'issueAction': request.json['issueAction'],
            'issueUser': request.json['issueUser'],
            'issueTime': request.json['issueTime'],
            'issueUpdateTime': request.json['issueUpdateTime'],
            'issueAssignee': request.json['issueAssignee'],
            'issueLabel': request.json['issueLabel'],
            'issueTitle': request.json['issueTitle'],
            'issueContent': request.json['issueContent'],
            'repoInfo': repoInfo,
        }

        res = requests.post(RULE_HANDLER_URL, json=rule_req_obj)
        print("print messages for debugging")
        print(res)
        if res.status_code >= 300:
            logger.error(f'error status_code: {res.status_code}, content: {res.text}')
            return "Internal Error", 500

        for rule_json in res.json():
            #rule_json = res.json()[0] # TODO Is the rule object a list or dict?
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
                'repoInfo': repoInfo
            }


            logging.debug(json.dumps(event_obj, indent=4))

            # TODO Get delay by comparing the current time and event_obj.pushTime
            target_time = datetime.strptime(rule_json['exeTime'], "%Y-%m-%dT%H:%M:%S%z")
            now = datetime.now(tz=target_time.tzinfo)
            diff = target_time - now
            delay = 0 if diff.total_seconds() <= 0 else diff.total_seconds()
            push_event(json.dumps(event_obj), delay=delay)

        #executor_res = requests.post(STRATEGY_EXECUTOR_URL, json.dumps(event_obj))
        #logging.debug(f'res.status: {executor_res.status_code}')
        #logging.debug(f'res.text: {executor_res.text}')
        return "", 200

    def get(self):
        pass
