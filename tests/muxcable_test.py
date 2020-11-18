import os
import traceback

from click.testing import CliRunner
from unittest import mock

import config.main as config
import config.main as config
import show.main as show
import mock_tables.dbconnector
from utilities_common.db import Db

tabular_data_status_output_expected = """PORT        STATUS    HEALTH
----------  --------  --------
Ethernet32  active    HEALTHY
Ethernet0   active    HEALTHY
"""

json_data_status_output_expected = """{
    "MUX_CABLE": {
        "Ethernet32": {
            "STATUS": "active",
            "HEALTH": "HEALTHY"
        },
        "Ethernet0": {
            "STATUS": "active",
            "HEALTH": "HEALTHY"
        }
    }
}
"""


tabular_data_config_output_expected = """SWITCH_NAME    PEER_TOR
-------------  ----------
sonic-switch   10.2.2.2
port        state    ipv4      ipv6
----------  -------  --------  --------
Ethernet32  active   10.1.1.1  fc00::75
Ethernet0   auto     10.2.1.1  e800::46
"""

json_data_status_config_output_expected = """{
    "MUX_CABLE": {
        "PEER_TOR": "10.2.2.2",
        "PORTS": {
            "Ethernet32": {
                "STATE": "active",
                "SERVER": {
                    "IPv4": "10.1.1.1",
                    "IPv6": "fc00::75"
                }
            },
            "Ethernet0": {
                "STATE": "auto",
                "SERVER": {
                    "IPv4": "10.2.1.1",
                    "IPv6": "e800::46"
                }
            }
        }
    }
}
"""

json_port_data_status_config_output_expected = """{
    "MUX_CABLE": {
        "PEER_TOR": "10.2.2.2",
        "PORTS": {
            "Ethernet32": {
                "STATE": "active",
                "SERVER": {
                    "IPv4": "10.1.1.1",
                    "IPv6": "fc00::75"
                }
            }
        }
    }
}
"""

json_data_config_output_auto_expected = """{
    "Ethernet0": "OK",
    "Ethernet1": "OK"
}
"""

json_data_config_output_active_expected = """{
    "Ethernet0": "OK",
    "Ethernet1": "INPROGRESS"
}
"""


class TestMuxcable(object):
    @classmethod
    def setup_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "1"
        print("SETUP")

    def test_muxcable_status(self):
        runner = CliRunner()
        db = Db()
        result = runner.invoke(show.cli.commands["muxcable"].commands["status"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == tabular_data_status_output_expected)

    def test_muxcable_status_json(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(show.cli.commands["muxcable"].commands["status"], ["--json"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == json_data_status_output_expected)

    def test_muxcable_status_config(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(show.cli.commands["muxcable"].commands["config"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == tabular_data_config_output_expected)

    def test_muxcable_status_config_json(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(show.cli.commands["muxcable"].commands["config"], ["--json"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == json_data_status_config_output_expected)

    def test_muxcable_status_config_json_port(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(show.cli.commands["muxcable"].commands["config"], ["Ethernet33", "--json"], obj=db)

        assert(result.exit_code == 1)

    def test_muxcable_config_json(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(config.config.commands["muxcable"].commands["mode"], ["auto","all","--json"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == json_data_config_output_auto_expected)

    def test_muxcable_config_json(self):
        runner = CliRunner()
        db = Db()

        result = runner.invoke(config.config.commands["muxcable"].commands["mode"], ["active","all","--json"], obj=db)

        assert(result.exit_code == 0)
        assert(result.output == json_data_config_output_active_expected)

    @classmethod
    def teardown_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "0"
        print("TEARDOWN")
