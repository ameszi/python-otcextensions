#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''CSS ELK cluster v1 action implementations'''
import logging
import base64

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class DownloadCert(command.Command):
    _description = _('Download the HTTPS certificate file of the server.')

    def get_parser(self, prog_name):
        parser = super(DownloadCert, self).get_parser(prog_name)
        parser.add_argument(
            '--out',
            metavar='<out>',
            required=True,
            help=_('Name of the output file where certificate will be saved.\n'
                   'Note: the file will be overwritten if it already exists')
        )

    def take_action(self, parsed_args):
        client = self.app.client_manager.css

        obj = client.get_certificate()
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)
        with open(parsed_args.out, 'wb') as cert_file:
            cert_file.write(base64.b64decode(data.cert_base64))
