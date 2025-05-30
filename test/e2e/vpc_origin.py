# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may
# not use this file except in compliance with the License. A copy of the
# License is located at
#
# 	 http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

"""Utilities for working with VpcOrigin resources"""

import datetime
import time

import boto3
import pytest

DEFAULT_WAIT_UNTIL_EXISTS_TIMEOUT_SECONDS = 60 * 10
DEFAULT_WAIT_UNTIL_EXISTS_INTERVAL_SECONDS = 15
DEFAULT_WAIT_UNTIL_DELETED_TIMEOUT_SECONDS = 60 * 10
DEFAULT_WAIT_UNTIL_DELETED_INTERVAL_SECONDS = 15


def wait_until_exists(
    vpc_origin_id: str,
    timeout_seconds: int = DEFAULT_WAIT_UNTIL_EXISTS_TIMEOUT_SECONDS,
    interval_seconds: int = DEFAULT_WAIT_UNTIL_EXISTS_INTERVAL_SECONDS,
) -> None:
    """Waits until a VpcOrigin with a supplied ID is returned from
    CloudFront GetVpcOrigin API.

    Usage:
        from e2e.vpc_origin import wait_until_exists

        wait_until_exists(vpc_origin_id)

    Raises:
        pytest.fail upon timeout
    """
    now = datetime.datetime.now()
    timeout = now + datetime.timedelta(seconds=timeout_seconds)

    while True:
        if datetime.datetime.now() >= timeout:
            pytest.fail(
                "Timed out waiting for VpcOrigin to exist "
                "in CloudFront API"
            )
        time.sleep(interval_seconds)

        latest = get(vpc_origin_id)
        if latest is not None:
            break


def wait_until_deleted(
    vpc_origin_id: str,
    timeout_seconds: int = DEFAULT_WAIT_UNTIL_DELETED_TIMEOUT_SECONDS,
    interval_seconds: int = DEFAULT_WAIT_UNTIL_DELETED_INTERVAL_SECONDS,
) -> None:
    """Waits until a VpcOrigin with a supplied ID is no longer returned from
    the CloudFront API.

    Usage:
        from e2e.vpc_origin import wait_until_deleted

        wait_until_deleted(vpc_origin_id)

    Raises:
        pytest.fail upon timeout
    """
    now = datetime.datetime.now()
    timeout = now + datetime.timedelta(seconds=timeout_seconds)

    while True:
        if datetime.datetime.now() >= timeout:
            pytest.fail(
                "Timed out waiting for VpcOrigin to be "
                "deleted in CloudFront API"
            )
        time.sleep(interval_seconds)

        latest = get(vpc_origin_id)
        if latest is None:
            break


def get(vpc_origin_id):
    """Returns a dict containing the VpcOrigin record from the CloudFront
    API.

    If no such VpcOrigin exists, returns None.
    """
    c = boto3.client("cloudfront")
    try:
        resp = c.get_vpc_origin(Id=vpc_origin_id)
        return resp["VpcOrigin"]
    except c.exceptions.EntityNotFound:
        return None