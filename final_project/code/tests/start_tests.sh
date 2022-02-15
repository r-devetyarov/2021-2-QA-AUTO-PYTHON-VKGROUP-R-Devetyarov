#!/bin/bash

pytest -s -l -v tests/ -m "${MARKS:API}" -n "${THREADS:0}" --alluredir /tmp/allure