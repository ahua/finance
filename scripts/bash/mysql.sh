#!/usr/bin/env bash

mysqldump -uadmin -padmin finance > finance.sql
mysql finance < finance.sql
