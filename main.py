from limon.metrics import Counter
from limon.exposition import generate_latest


if __name__ == '__main__':
    http_requests = Counter(
        'http_request',
        'Count of http requests',
        ['method', 'endpoint']
    )
    http_requests.labels('post', '/auth').inc()
    http_requests.labels('get', '/metrics').inc(3)
    print(generate_latest())
