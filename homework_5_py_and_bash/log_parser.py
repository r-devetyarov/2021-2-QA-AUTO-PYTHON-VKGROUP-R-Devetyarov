import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Dict, List

METHODS = ("GET", "POST", "PUT", "DELETE", "PATH", "CONNECT", "OPTIONS", "TRACE", "HEAD")
BAD_REQUEST_RC = tuple(i for i in range(400, 500))
SERVER_ERROR_RC = tuple(i for i in range(500, 600))


class PathDoesNotExist(Exception):
    pass


class Params(NamedTuple):
    path: Path = Path()
    json: str = ''
    bad_request_max_size: int = 0
    top_users_server_error: int = 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", '-p', help="Path to log file", default='access.log')
    parser.add_argument("--json", '-J', help="Save results to json filename", action="store_true")
    parser.add_argument("--bad_request_max_size", '-br', help="Save results to json filename", default="5")
    parser.add_argument("--top_users_server_error", '-tu', help="Save results to json filename", default="5")

    args = parser.parse_args()
    params = Params(path=args.path,
                    json=args.json,
                    bad_request_max_size=int(args.bad_request_max_size),
                    top_users_server_error=int(args.top_users_server_error))
    return params


def log_parser():
    params = parse_args()
    if not Path(params.path).exists():
        raise PathDoesNotExist(f'{params.path} doens\'t exists')

    method_count = {"methods_count": {f"count_{key.lower()}": 0 for key in METHODS}}
    url_list = []
    bad_requests = []
    server_error = []
    line_count = 0

    with Path(params.path).open('r', encoding="utf-8") as log:
        for line in log:
            nginx_log = nginx_line_parser(line)

            line_count += 1
            method_count["methods_count"][f"count_{nginx_log.method.lower()}"] += 1
            url_list.append(nginx_log.url)

            if nginx_log.status_code in BAD_REQUEST_RC:
                bad_requests.append(
                    dict(request_ip=nginx_log.ip, rs_status_code=nginx_log.status_code,
                         request_size=nginx_log.request_count,
                         requst_url=nginx_log.url))

            if nginx_log.status_code in SERVER_ERROR_RC:
                server_error.append(nginx_log.ip)

    results = collector_results(
        method_count=method_count,
        url_list=url_list,
        bad_requests=bad_requests,
        server_error=server_error,
        line_count=line_count,
        params=params)

    if params.json:
        save_to_json(results)
    else:
        save_to_txt(results)


def collector_results(method_count: Dict, url_list: List, bad_requests: List, server_error: List, line_count: int,
                      params: Params):
    results = {"line_count": line_count}
    results.update(method_count)
    mcu = Counter(url_list).most_common()[0]
    results.update({"most_common_url": {"url": mcu[0], "counts": mcu[1]}})
    bad_request_size = list(sorted(bad_requests, key=lambda request: request["request_size"], reverse=True))[
                       :params.bad_request_max_size]
    results.update({f"bad_request_top_{params.bad_request_max_size}_max_size": bad_request_size})
    server_error_top_ip = Counter(server_error).most_common()[:params.top_users_server_error]
    results.update(
        {f"top_{params.top_users_server_error}_ip_server_error": {ip[0]: ip[1] for ip in server_error_top_ip}})
    return results


class NginxParams(NamedTuple):
    ip: str = ''
    url: str = ''
    method: str = ''
    status_code: int = 0
    request_count: int = 0


def nginx_line_parser(line_nginx_log: str) -> NginxParams:
    split_line = line_nginx_log.split(" ")
    ip = split_line[0]
    url = split_line[6].replace('"', '')
    method = split_line[5].replace('"', '')
    if method not in METHODS:
        # для случая когда метод запроса записан слитно (1 такой случай)
        method = [met for met in METHODS if met in method[-10:]][0]
    status_code = int(split_line[8])
    if split_line[9] == "-":
        request_count = 0
    else:
        request_count = int(split_line[9])

    return NginxParams(ip=ip, url=url, method=method, status_code=status_code, request_count=request_count)


def save_to_txt(results: Dict):
    for key, value in results.items():
        with open(f'results_{str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))}.txt', 'a') as file:
            file.write(f"{key}\n{value}\n")


def save_to_json(results: Dict):
    with open(f'results_{str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))}.json', 'w') as file:
        json.dump(results, file)


if __name__ == "__main__":
    log_parser()
