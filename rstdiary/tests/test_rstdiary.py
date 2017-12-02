"""
test_rstdiary
-------------

Tests for `rstdiary` module
"""

import configparser
import fixtures
import os
import testtools

from testtools.matchers import FileExists

from rstdiary import rstdiary


class TestRstdiary(testtools.TestCase):

    def test_output(self):
        # Simple test of parsing and output
        test_dir = self.useFixture(fixtures.TempDir()).path

        # Handy for testing strptime, but not always available
        # ---
        # import locale
        # locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

        results = rstdiary.parse_entries('rstdiary/tests/sample/basic.rst')
        fake_config = configparser.ConfigParser()
        fake_config.read_dict({
            'rstdiary': {
                'title': 'test title',
                'about': 'test about',
                'output_dir': test_dir}
        })

        config_fixture = fixtures.MockPatchObject(rstdiary,
                                                  'config', fake_config)

        with config_fixture:
            rstdiary.write_html(**results)

        # TODO(ianw): better testing
        self.assertThat(os.path.join(test_dir, 'index.html'), FileExists())
