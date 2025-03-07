# -*- coding: utf-8 -*-
#
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - API 网关(BlueKing - APIGateway) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.
#
import pytest
from tests.utils.testing import get_response_json

from apigateway.apps.docs.gateway.resource import views


class TestResourceViewSet:
    @pytest.mark.parametrize(
        "mocked_api, mocked_resources, api_name, stage_name, will_error, expected",
        [
            (
                {"id": 1},
                {
                    "count": 1,
                    "results": [
                        {
                            "id": 1,
                            "name": "test",
                            "description": "desc",
                            "method": "POST",
                            "path": "/test/",
                            "app_verified_required": True,
                            "resource_perm_required": True,
                            "user_verified_required": True,
                            "labels": [],
                        },
                    ],
                },
                "api-test",
                "prod",
                False,
                {
                    "count": 1,
                    "results": [
                        {
                            "id": 1,
                            "name": "test",
                            "description": "desc",
                            "method": "POST",
                            "path": "/test/",
                            "app_verified_required": True,
                            "resource_perm_required": True,
                            "user_verified_required": True,
                            "labels": [],
                        }
                    ],
                },
            ),
            # api not exist
            (
                {},
                {
                    "count": 1,
                    "results": [
                        {
                            "id": 1,
                            "name": "test",
                            "description": "desc",
                            "method": "POST",
                            "path": "/test/",
                            "app_verified_required": True,
                            "resource_perm_required": True,
                            "user_verified_required": True,
                            "labels": [],
                        },
                    ],
                },
                "api-test",
                "prod",
                True,
                None,
            ),
        ],
    )
    def test_list(
        self,
        mocker,
        request_factory,
        mocked_api,
        mocked_resources,
        api_name,
        stage_name,
        will_error,
        expected,
    ):
        mocked_get_gateway_by_name = mocker.patch(
            "apigateway.apps.docs.gateway.resource.views.support_helper.get_gateway_by_name",
            return_value=mocked_api,
        )
        mocked_get_released_resources = mocker.patch(
            "apigateway.apps.docs.gateway.resource.views.support_helper.get_released_resources",
            return_value=mocked_resources,
        )

        request = request_factory.get("")
        view = views.ResourceViewSet.as_view({"get": "list"})
        response = view(request, api_name, stage_name)
        result = get_response_json(response)

        if will_error:
            assert response.status_code == 404
            assert result["code"] == 40404
            return

        assert result["code"] == 0
        assert result["data"] == expected

        mocked_get_gateway_by_name.assert_called_once_with(api_name)
        mocked_get_released_resources.assert_called_once_with(
            mocked_api["id"],
            stage_name,
        )
