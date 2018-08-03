#StatusPage Agent

The objective of statuspage-agent is to provide a flexible way to handle requests within a complex Internal Status Page API application. 


##Installation

1.  install via `pip install statuspage-agent`


##Basic Usage

Here's an example:

__example.py__
    
    client = Client('https://statuspage.example.com/v1/incident/deadbeefdeadbeef/', 'My Group Name.My Component')
    try:
        ...  # your logic
        client.send_heartbeat()  # when success
    except Exception:
        client.send_heartbeat(status=Client.STATUS_WARNING)  # when failed

__another_example.py__

    client = Client('https://statuspage.example.com/v1/incident/deadbeefdeadbeef/')
    try:
        ...  # your logic
        client.send_heartbeat('My Group Name.My Component')  # when success
    except Exception:
        client.send_heartbeat('My Group Name.My Component', status=Client.STATUS_ERROR, 'Validation Failured', 'lorem ipsum')  # when failed


##Advanced Usage

If you need more status. Here's all of statuses:

__example.py__

    Client.STATUS_OPERATIONAL
    Client.STATUS_DEGRADED_PERFORMANCE
    Client.STATUS_PARTIAL_OUTAGE
    Client.STATUS_MAJOR_OUTAGE
    Client.STATUS_UNDER_MAINTENANCE
    Client.STATUS_WARNING  # same as STATUS_DEGRADED_PERFORMANCE
    Client.STATUS_ERROR  # same as STATUS_PARTIAL_OUTAGE
    Client.STATUS_CRITICAL  # same as STATUS_MAJOR_OUTAGE
