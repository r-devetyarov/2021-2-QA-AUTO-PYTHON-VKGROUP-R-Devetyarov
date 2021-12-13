from typing import List

from models.model import (BadRequestTopMaxSize, LineCount, MethodsCount,
                          MostCommonUrl, ServerErrorTopIp)
from test_sql.base_case import MysqlBase


class TestLineCount(MysqlBase):
    def prepare(self):
        self.mysql.insert_data(
            LineCount, line_count=self.log_parser_result["line_count"]
        )

    def test_line_count(self):
        all_line_count = self.all_query(LineCount)
        assert len(all_line_count) == 1
        assert all_line_count[0].line_count == self.log_parser_result["line_count"]


class TestMethodsCount(MysqlBase):
    def prepare(self):
        for method_name, method_count in self.log_parser_result[
            "methods_count"
        ].items():
            self.mysql.insert_data(
                MethodsCount, method_name=method_name, method_count=method_count
            )

    def test_methods_count(self):
        all_methods_count = self.all_query(MethodsCount)
        assert len(all_methods_count) == len(self.log_parser_result["methods_count"])
        for method in all_methods_count:
            method: MethodsCount
            assert (
                method.method_count
                == self.log_parser_result["methods_count"][method.method_name]
            )


class TestMostCommonUrl(MysqlBase):
    def prepare(self):
        self.mysql.insert_data(
            MostCommonUrl,
            url=self.log_parser_result["most_common_url"]["url"],
            count=self.log_parser_result["most_common_url"]["counts"],
        )

    def test_most_common_url(self):
        all_most_common_url = self.all_query(MostCommonUrl)
        assert len(all_most_common_url) == 1
        all_most_common_url: List[MostCommonUrl]
        assert (
            all_most_common_url[0].url
            == self.log_parser_result["most_common_url"]["url"]
        )
        assert (
            all_most_common_url[0].count
            == self.log_parser_result["most_common_url"]["counts"]
        )


class TestBadRequestTopMaxSize(MysqlBase):
    def prepare(self):

        for request in self.log_parser_result["bad_request_top_5_max_size"]:
            self.mysql.insert_data(
                BadRequestTopMaxSize,
                request_ip=request["request_ip"],
                response_rc=request["rs_status_code"],
                request_size=request["request_size"],
                request_url=request["request_url"],
            )

    def test_bad_request_top_max_size(self):
        all_bad_request = self.all_query(BadRequestTopMaxSize)
        all_bad_request: List[BadRequestTopMaxSize]
        len(all_bad_request) == len(
            self.log_parser_result["bad_request_top_5_max_size"]
        )
        for i in range(len(all_bad_request)):
            assert (
                all_bad_request[i].request_ip
                == self.log_parser_result["bad_request_top_5_max_size"][i]["request_ip"]
            )
            assert (
                all_bad_request[i].request_size
                == self.log_parser_result["bad_request_top_5_max_size"][i][
                    "request_size"
                ]
            )
            assert (
                all_bad_request[i].response_rc
                == self.log_parser_result["bad_request_top_5_max_size"][i][
                    "rs_status_code"
                ]
            )
            assert (
                all_bad_request[i].request_url
                == self.log_parser_result["bad_request_top_5_max_size"][i][
                    "request_url"
                ]
            )


class TestServerErrorTopIp(MysqlBase):
    def prepare(self):
        for ip, count in self.log_parser_result["top_5_ip_server_error"].items():
            self.mysql.insert_data(
                ServerErrorTopIp,
                request_ip=ip,
                count=count,
            )

    def test_server_error_top_ip(self):
        all_server_error = self.all_query(ServerErrorTopIp)
        all_server_error: List[ServerErrorTopIp]
        assert len(all_server_error) == len(self.log_parser_result["top_5_ip_server_error"])
        for error in all_server_error:
            assert error.count == self.log_parser_result["top_5_ip_server_error"][error.request_ip]
