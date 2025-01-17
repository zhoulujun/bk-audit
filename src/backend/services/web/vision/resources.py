# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 审计中心 (BlueKing - Audit Center) available.
Copyright (C) 2023 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.
We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""

import abc

from bk_resource import Resource
from django.utils.translation import gettext_lazy
from rest_framework.generics import get_object_or_404

from services.web.vision.handlers.query import VisionHandler
from services.web.vision.models import VisionPanel
from services.web.vision.serializers import (
    QueryMetaReqSerializer,
    VisionPanelInfoSerializer,
)


class BKVision(Resource, abc.ABC):
    tags = ["BKVision"]


class ListPanels(BKVision):
    name = gettext_lazy("仪表盘列表")
    ResponseSerializer = VisionPanelInfoSerializer
    many_response_data = True

    def perform_request(self, validated_request_data):
        return VisionPanel.objects.all()


class QueryMeta(BKVision):
    name = gettext_lazy("查询视图配置")
    RequestSerializer = QueryMetaReqSerializer

    def perform_request(self, validated_request_data):
        get_object_or_404(VisionPanel, id=validated_request_data.get("share_uid"))
        return VisionHandler().query_meta(params=validated_request_data)


class QueryData(BKVision):
    name = gettext_lazy("获取面板视图数据")

    def perform_request(self, validated_request_data):
        get_object_or_404(VisionPanel, id=validated_request_data.get("share_uid"))
        return VisionHandler().query_data(params=validated_request_data)
