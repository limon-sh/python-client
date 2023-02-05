from limon.metrics import Counter
from limon.exposition import generate_latest


if __name__ == '__main__':
    http_requests = Counter(
        'http_total_request',
        'Count of http requests',
        {'host': 'localhost'}
    )
    http_requests.inc(2)
    print(generate_latest())
