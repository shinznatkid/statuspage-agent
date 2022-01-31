from threading import Thread
import datetime
import logging
import socket

import requests


HOST_NAME = socket.gethostname()


class Client(object):
    '''
    Status page Client

    Minimum usage:

        client = Client('https://www.example.com/v1/incident/deadbeefdeadbeef/', 'My Group.My component')
        client.send_heartbeat()

    Example other usage:

        client = Client('https://www.example.com/v1/incident/deadbeefdeadbeef/')
        client.send_heartbeat('My Group.My component')

        client = Client('https://www.example.com/v1/incident/deadbeefdeadbeef/')
        client.send_heartbeat('My Group.My component', heartbeat_duration='00:10:00')

        client = Client('https://www.example.com/v1/incident/deadbeefdeadbeef/')
        client.send_heartbeat('My Group.My component', status=Client.STATUS_WARNING)

        client = Client('https://www.example.com/v1/incident/deadbeefdeadbeef/')
        client.send_heartbeat('My Group.My component', status=Client.STATUS_ERROR, 'Validation Failured', 'lorem ipsum')

    '''

    STATUS_OPERATIONAL = 'operational'
    STATUS_DEGRADED_PERFORMANCE = 'degraded_performance'
    STATUS_PARTIAL_OUTAGE = 'partial_outage'
    STATUS_MAJOR_OUTAGE = 'major_outage'
    STATUS_UNDER_MAINTENANCE = 'under_maintenance'

    STATUS_WARNING = STATUS_DEGRADED_PERFORMANCE   # Shortcut
    STATUS_ERROR = STATUS_PARTIAL_OUTAGE   # Shortcut
    STATUS_CRITICAL = STATUS_MAJOR_OUTAGE   # Shortcut

    STATUS_LIST = (
        STATUS_OPERATIONAL,
        STATUS_DEGRADED_PERFORMANCE,
        STATUS_PARTIAL_OUTAGE,
        STATUS_MAJOR_OUTAGE,
        STATUS_UNDER_MAINTENANCE,
    )

    def __init__(self, data_source, default_component_name=None, default_heartbeat_duration=None, send_async=True, logger=None, allow_insecure=False):
        self.data_source = data_source
        self.default_component_name = default_component_name

        if isinstance(default_heartbeat_duration, datetime.time) or isinstance(default_heartbeat_duration, datetime.datetime):
            default_heartbeat_duration = default_heartbeat_duration.strftime('%H:%M:%S')
        self.default_heartbeat_duration = default_heartbeat_duration

        self.logger = logger or logging.getLogger('statuspage')
        self._log_thread = None
        self.send_async = send_async
        self.allow_insecure = allow_insecure

    def send_heartbeat(self, component_name=None, status='operational', issue_name='', issue_description='', heartbeat_duration=None, action_datetime=None, is_send_notification=True, hostname=None):

        if not self.data_source:
            self.logger.warning('data source is not set.')
            return

        component_name = component_name or self.default_component_name
        if not component_name:
            raise ValueError('component_name required.')

        status = status or 'operational'  # default
        if status not in self.STATUS_LIST:
            raise ValueError('invalid status.')

        heartbeat_duration = heartbeat_duration or self.default_heartbeat_duration
        if isinstance(heartbeat_duration, datetime.time):
            heartbeat_duration = heartbeat_duration.strftime('%H:%M:%S')

        if isinstance(action_datetime, datetime.date) or isinstance(action_datetime, datetime.datetime):
            action_datetime = action_datetime.strftime('%Y-%m-%d %H:%M:%S')
        elif not action_datetime:
            action_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not hostname:
            hostname = HOST_NAME

        data = {
            'component': component_name,
            'status': status,
            'is_send_notification': is_send_notification,
            'hostname': hostname,
        }
        if heartbeat_duration:
            data['heartbeat_duration'] = heartbeat_duration
        if issue_description:
            data['issue_description'] = issue_description
        if issue_name:
            data['issue_name'] = issue_name
        if action_datetime:
            data['date'] = action_datetime

        if self.send_async:
            self._async_send_log(data)
        else:
            self._send_log(data)

    def _async_send_log(self, data):

        def _async_log():
            self._send_log(data)

        self._log_thread = Thread(target=_async_log)
        self._log_thread.start()

    def _send_log(self, data):
        is_verify = not self.allow_insecure
        response = requests.post(self.data_source, json=data, verify=is_verify)
        self.logger.debug('status code = %s', response.status_code)
        if 400 <= response.status_code < 500:
            self.logger.warning('Cannot send statuspage: status code %s\n%s', response.status_code, response.text)
        if 500 <= response.status_code < 600:
            self.logger.warning('Cannot send statuspage: status code %s\n%s', response.status_code, response.text)
