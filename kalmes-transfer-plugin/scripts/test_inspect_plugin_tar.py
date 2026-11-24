#!/usr/bin/env python3
"""Synthetic archive regressions; no extraction, code execution or Kalmes access."""

import io
import json
import tempfile
import unittest
from pathlib import Path
import tarfile

from inspect_plugin_tar import DEFAULT_MAX_BYTES, DEFAULT_MAX_MEMBERS, inspect_archive


class DeploymentRoutingTests(unittest.TestCase):
    def inspect(self, flat=False, query='', *, wrapper='arbitrary-wrapper', html=True,
                module='DemoPortal', expected_pages=(), omit_flat=False):
        meta = {
            'plugin_name': 'demo', 'version': '1.2.0', 'flat': flat,
            'expose': False, 'files': [{'name': 'DemoApi.py', 'type': 'API'}],
            'override': [], 'env': [], 'fap_ds': [],
        }
        sources = {'DemoApi.py': b'def invoke(*args, **kwargs):\n    return 200, {}\n'}
        if html:
            meta['files'].append({'name': 'DemoPortal.py', 'type': 'Html'})
            meta['override'].append({
                'name_key': 'DemoPortal',
                'target_url': f'/project/api/extracode/html/preview/{module}{query}',
            })
            sources['DemoPortal.py'] = b'def invoke(*args, **kwargs):\n    return "demo"\n'
        if omit_flat:
            del meta['flat']
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'renamed-download.tar'
            prefix = wrapper + '/' if wrapper else ''
            with tarfile.open(path, 'w') as archive:
                content = {prefix + 'meta.json': json.dumps(meta).encode('utf-8')}
                content.update({prefix + 'files/' + name: data for name, data in sources.items()})
                for name, data in content.items():
                    entry = tarfile.TarInfo(name)
                    entry.size = len(data)
                    archive.addfile(entry, io.BytesIO(data))
            return inspect_archive(path, DEFAULT_MAX_MEMBERS, DEFAULT_MAX_BYTES, expected_pages)

    def assert_warning(self, result, fragment):
        self.assertTrue(any(fragment in warning for warning in result['warnings']), result)

    def test_versioned_selector_matches_manifest_not_wrapper_or_download(self):
        result = self.inspect(query='?action=view&plugin=demo1.2.0', expected_pages=('DemoPortal',))
        self.assertTrue(result['valid'])
        self.assertEqual(result['deployment_mode'], 'versioned')
        self.assertEqual(result['expected_install_folder'], 'demo1.2.0')
        self.assertEqual(result['warnings'], [])

    def test_missing_versioned_selector_warns_without_rejecting_archive(self):
        result = self.inspect()
        self.assertTrue(result['valid'])
        self.assert_warning(result, 'no non-empty plugin selector')

    def test_empty_versioned_selector_warns(self):
        result = self.inspect(query='?plugin=')
        self.assertTrue(result['valid'])
        self.assert_warning(result, 'no non-empty plugin selector')

    def test_source_folder_left_in_upgrade_target_warns(self):
        result = self.inspect(query='?plugin=demo1.1.0')
        self.assertTrue(result['valid'])
        self.assert_warning(result, 'differs from the expected install folder')

    def test_flat_without_selector_uses_shared_folder(self):
        result = self.inspect(flat=True)
        self.assertTrue(result['valid'])
        self.assertEqual(result['deployment_mode'], 'shared')
        self.assertEqual(result['expected_install_folder'], '.')
        self.assertEqual(result['warnings'], ['flat=true installs into the shared extraCode directory'])

    def test_flat_with_stale_folder_warns(self):
        result = self.inspect(flat=True, query='?plugin=demo1.1.0')
        self.assertTrue(result['valid'])
        self.assert_warning(result, 'flat=true page selects a plugin folder')

    def test_blank_selector_in_flat_mode_does_not_warn_about_stale_folder(self):
        result = self.inspect(flat=True, query='?plugin=&action=view')
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['warnings']), 1)

    def test_duplicate_selectors_are_ambiguous_even_if_identical(self):
        for query in ('?plugin=demo1.2.0&plugin=demo1.2.0', '?plugin=&plugin=demo1.2.0'):
            with self.subTest(query=query):
                result = self.inspect(query=query)
                self.assertTrue(result['valid'])
                self.assert_warning(result, 'ambiguous plugin query parameters')

    def test_encoded_selector_and_unrelated_query_values(self):
        result = self.inspect(query='?plugin=demo1%2E2%2E0&return=somewhere&action=view')
        self.assertTrue(result['valid'])
        self.assertEqual(result['warnings'], [])

    def test_missing_flat_does_not_assume_runtime_routing(self):
        result = self.inspect(omit_flat=True)
        self.assertTrue(result['valid'])
        self.assertEqual(result['deployment_mode'], 'unspecified')
        self.assertIsNone(result['expected_install_folder'])
        self.assert_warning(result, 'flat is not an explicit boolean')

    def test_non_boolean_flat_does_not_assume_runtime_routing(self):
        result = self.inspect(flat='false')
        self.assertEqual(result['deployment_mode'], 'unspecified')
        self.assert_warning(result, 'flat is not an explicit boolean')

    def test_api_only_archive_needs_no_page_selector(self):
        result = self.inspect(html=False)
        self.assertTrue(result['valid'])
        self.assertEqual(result['warnings'], [])

    def test_root_level_archive_uses_manifest_folder(self):
        result = self.inspect(wrapper='', query='?plugin=demo1.2.0')
        self.assertTrue(result['valid'])
        self.assertEqual(result['expected_install_folder'], 'demo1.2.0')
        self.assertEqual(result['warnings'], [])

    def test_mismatched_module_remains_structural_error(self):
        result = self.inspect(module='OtherPortal', query='?plugin=demo1.2.0')
        self.assertFalse(result['valid'])
        self.assertTrue(any('no matching declared Html file' in error for error in result['errors']))

    def test_expected_page_still_required(self):
        result = self.inspect(html=False, expected_pages=('DemoPortal',))
        self.assertFalse(result['valid'])
        self.assertTrue(any('missing expected embedded page' in error for error in result['errors']))


if __name__ == '__main__':
    unittest.main()
