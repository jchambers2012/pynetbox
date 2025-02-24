import unittest
from unittest.mock import patch

import pynetbox

from .util import Response

host = "http://localhost:8000"

def_kwargs = {
    "token": "abc123",
}

endpoints = {
    "dcim": "devices",
    "ipam": "prefixes",
    "circuits": "circuits",
}

class ApiBranchingTestCase(unittest.TestCase):
    class ResponseWithBranching:
        ok = True

        def json(self):
            return {
                "netbox-version": "0.9.9",
                "plugins": {
                    "netbox_branching": "0.5.2",
                },
            }
    class ResponseMissingBranching:
        ok = True

        def json(self):
            return {
                "netbox-version": "0.9.9",
            }

    @patch(
        "requests.sessions.Session.get",
        return_value=ResponseWithBranching(),
    )
    def test_api_has_branching(self, *_):
        api = pynetbox.api(
            host,
        )
        self.assertEqual(api.has_branching, None)
        api.status()
        self.assertTrue(api.has_branching)

    @patch(
        "requests.sessions.Session.get",
        return_value=ResponseMissingBranching(),
    )
    def test_api_has_branching(self, *_):
        api = pynetbox.api(
            host,
        )
        self.assertEqual(api.has_branching, None)
        api.status()
        self.assertFalse(api.has_branching)
        with self.assertRaises(AttributeError) as e:
            api.branch_set(branch="test")
        self.assertEqual(str(e.exception), "Branching Plugin is not found NetBox")
        with self.assertRaises(AttributeError) as e:
            api.branch_ready(branch_schema="test")
        self.assertEqual(str(e.exception), "Branching Plugin is not found NetBox")
        with self.assertRaises(AttributeError) as e:
            api.branch_activate(branch_schema="test")
        self.assertEqual(str(e.exception), "Branching Plugin is not found NetBox")

    def test_api_branch_activate(self):
        api = pynetbox.api(
            host,
            **def_kwargs
        )
        
