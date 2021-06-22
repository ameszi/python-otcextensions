# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import uuid

import openstack

from otcextensions.tests.functional.sdk.cts import TestCts

_logger = openstack._log.setup_logging('openstack')


class TestTraces(TestCts):
    uuid_v4 = uuid.uuid4().hex[:8]
    tracker_name = 'system'
    tracker_prefix = f'{uuid_v4}-cts-sdk-'
    bucket_name = uuid_v4 + '-sdk-test'
    bucket = None

    def setUp(self):
        super(TestTraces, self).setUp()
        self._create_bucket()
        if self.bucket:
            try:
                self.tracker = self.client.create_tracker(
                    bucket_name=self.bucket_name,
                    file_prefix_name=self.tracker_prefix,
                )
            except openstack.exceptions.BadRequestException:
                self.tracker = self.client.get_tracker(self.tracker_name)

    def tearDown(self):
        super(TestTraces, self).tearDown()
        if self.bucket:
            self._delete_bucket()
        try:
            if self.tracker:
                self.client.delete_tracker(self.tracker)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def _create_bucket(self):
        self.bucket = self.obs_client.create_container(name=self.bucket_name)
        self.obs_client.containers()

    def _delete_bucket(self):
        if self.bucket:
            self.obs_client.delete_container(container=self.bucket)

    def test_list_traces(self):
        traces = self.client.traces()
        self.assertIsNotNone(traces)
        tr = next(traces)
        self.assertEqual(tr['tracker_name'], self.tracker_name)
        self.assertEqual(tr['service_type'], 'CTS')

    def test_get_tracker(self):
        tracker = self.client.get_tracker(self.tracker_name)
        self.assertEqual(tracker['file_prefix_name'], self.tracker_prefix)
        self.assertEqual(tracker['bucket_name'], self.bucket_name)

    def test_update_tracker(self):
        new_prefix = f'{self.uuid_v4}-cts-sdk-new-'
        tracker = self.client.get_tracker(self.tracker_name)
        self.assertEqual(tracker['file_prefix_name'], self.tracker_prefix)
        tracker = self.client.update_tracker(
            tracker=self.tracker_name,
            file_prefix_name=new_prefix
        )
        self.assertEqual(tracker['file_prefix_name'], new_prefix)
