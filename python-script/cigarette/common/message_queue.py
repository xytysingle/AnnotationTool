import redis
import json
from logger import setup_logging
import yaml


logger = setup_logging(__name__)

with open('redis.yaml') as fr:
    redis_cfg = yaml.load(fr)
host = redis_cfg['host']
port = redis_cfg['port']
db = redis_cfg['db']
r = redis.StrictRedis(host=host, port=port, db=db)


def enqueue(queue_name, data):
    value = json.dumps(data)
    return r.lpush(queue_name, value)


def dequeue(queue_name, block=True, timeout=0):
    if block:
        ret = r.brpop(queue_name, timeout)
        if ret is None:
            return None
        name, value = ret
    else:
        value = r.rpop(queue_name)
    return json.loads(value.decode('utf-8'), object_hook=_decode_dict) if value else None


def dequeue_timeout_warning_error(queue_name, timeout_warning=60, timeout_error=300):
    """
    Dequeue with timeout warning
    If not dequeued in `timeout` seconds, a warning email will send out.
    :param queue_name:
    :param timeout_warning:
    :param timeout_error:
    :return:
    """
    ret = dequeue(queue_name, block=True, timeout=timeout_warning)
    if ret is None:  # timeout
        logger.warning('Dequeue from {} timeout in {} seconds.'.format(queue_name, timeout_warning))
        timeout = timeout_error - timeout_warning
        ret = dequeue(queue_name, block=True, timeout=timeout)
        if ret is None:  # timeout
            raise Exception('Dequeue from {} timeout in {} seconds!'.format(queue_name, timeout))
        else:
            return ret
    else:
        return ret


def clear(queue_name):
    r.delete(queue_name)


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv
