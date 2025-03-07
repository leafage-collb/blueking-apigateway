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
from ddf import G

from apigateway.apis.open.resource_version import views
from apigateway.core.models import ResourceVersion
from apigateway.tests.utils.testing import get_response_json

pytestmark = pytest.mark.django_db


class TestResourceVersionViewSet:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, mocker):
        mocker.patch(
            "apigateway.apis.open.resource_version.views.GatewayRelatedAppPermission.has_permission",
            return_value=True,
        )

    def test_create(self, request_factory, fake_gateway, mocker):
        mocker.patch(
            "apigateway.apis.open.resource_version.views.ResourceVersionHandler.make_version",
            return_value=[{"name": "test"}],
        )
        mocker.patch(
            "apigateway.apps.resource_version.serializers.ResourceVersionSLZ._validate_resource_count",
            return_value=None,
        )

        request = request_factory.post(
            "",
            data={
                "title": "test",
            },
        )
        request.gateway = fake_gateway

        view = views.ResourceVersionViewSet.as_view({"post": "create"})
        response = view(request, fake_gateway.name)
        result = get_response_json(response)

        assert result["code"] == 0

    @pytest.mark.parametrize(
        "unreleased_stage_ids",
        [[], [1, 2]],
    )
    def test_release(self, faker, request_view, fake_admin_user, fake_gateway, mocker, unreleased_stage_ids):
        G(ResourceVersion, api=fake_gateway)
        mocker.patch(
            "apigateway.apis.open.resource_version.views.ReleaseBatchManager.release_batch",
            return_value=None,
        )
        mocker.patch(
            "apigateway.apis.open.resource_version.serializers.ReleaseV1SLZ.to_internal_value",
            return_value={
                "api": fake_gateway,
                "stage_ids": [1, 2],
                "resource_version_id": 1,
                "comment": "",
            },
        )
        mocker.patch(
            "apigateway.apis.open.resource_version.views.ResourceVersion.objects.get_object_fields",
            return_value={
                "id": faker.pyint(),
                "name": faker.pystr(),
                "title": faker.pystr(),
                "version": faker.pystr(),
            },
        )
        mocker.patch(
            "apigateway.apis.open.resource_version.views.Release.objects.get_stage_ids_unreleased_the_version",
            return_value=unreleased_stage_ids,
        )

        response = request_view(
            "POST",
            "openapi.resource_version.release",
            gateway=fake_gateway,
            path_params={
                "gateway_name": fake_gateway.name,
            },
            data={
                "stage_name": ["prod"],
                "resource_version_name": "test",
            },
            user=fake_admin_user,
        )

        result = get_response_json(response)
        assert result["code"] == 0

    def test_list(self, fake_resource_version, request_view):
        fake_gateway = fake_resource_version.api

        response = request_view(
            "GET",
            "openapi.resource_versions",
            gateway=fake_gateway,
            path_params={
                "gateway_name": fake_gateway.name,
            },
            data={
                "version": fake_resource_version.version,
            },
        )
        result = response.json()
        assert result["data"]["count"] == 1

        response = request_view(
            "GET",
            "openapi.resource_versions",
            gateway=fake_gateway,
            path_params={
                "gateway_name": fake_gateway.name,
            },
            data={
                "version": fake_resource_version.version + "-not-exists",
            },
        )
        result = response.json()
        assert result["data"]["count"] == 0
