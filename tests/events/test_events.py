# -*- coding: utf-8 -*-
# Copyright 2014 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from synapse.api.events import SynapseEvent

from tests import unittest


class SynapseTemplateCheckTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_top_level_keys(self):
        template = {
            "person": {},
            "friends": ["string"]
        }

        content = {
            "person": {"name": "bob"},
            "friends": ["jill", "mike"]
        }

        event = MockSynapseEvent(template)
        self.assertTrue(event.check_json(content, raises=False))

        content = {
            "person": {"name": "bob"},
            "friends": ["jill"],
            "enemies": ["mike"]
        }
        event = MockSynapseEvent(template)
        self.assertTrue(event.check_json(content, raises=False))

        content = {
            "person": {"name": "bob"},
            # missing friends
            "enemies": ["mike", "jill"]
        }
        self.assertFalse(event.check_json(content, raises=False))

    def test_lists(self):
        template = {
            "person": {},
            "friends": [{"name":"string"}]
        }

        content = {
            "person": {"name": "bob"},
            "friends": ["jill", "mike"]  # should be in objects
        }

        event = MockSynapseEvent(template)
        self.assertFalse(event.check_json(content, raises=False))

        content = {
            "person": {"name": "bob"},
            "friends": [{"name": "jill"}, {"name": "mike"}]
        }
        self.assertTrue(event.check_json(content, raises=False))

    def test_nested_lists(self):
        template = {
            "results": {
                "families": [
                     {
                        "name": "string",
                        "members": [
                            {}
                        ]
                     }
                ]
            }
        }

        content = {
            "results": {
                "families": [
                     {
                        "name": "Smith",
                        "members": [
                            "Alice", "Bob"  # wrong types
                        ]
                     }
                ]
            }
        }

        event = MockSynapseEvent(template)
        self.assertFalse(event.check_json(content, raises=False))

        content = {
            "results": {
                "families": [
                     {
                        "name": "Smith",
                        "members": [
                            {"name": "Alice"}, {"name": "Bob"}
                        ]
                     }
                ]
            }
        }
        self.assertTrue(event.check_json(content, raises=False))

    def test_nested_keys(self):
        template = {
            "person": {
                "attributes": {
                    "hair": "string",
                    "eye": "string"
                },
                "age": 0,
                "fav_books": ["string"]
            }
        }
        event = MockSynapseEvent(template)

        content = {
            "person": {
                "attributes": {
                    "hair": "brown",
                    "eye": "green",
                    "skin": "purple"
                },
                "age": 33,
                "fav_books": ["lotr", "hobbit"],
                "fav_music": ["abba", "beatles"]
            }
        }

        self.assertTrue(event.check_json(content, raises=False))

        content = {
            "person": {
                "attributes": {
                    "hair": "brown"
                    # missing eye
                },
                "age": 33,
                "fav_books": ["lotr", "hobbit"],
                "fav_music": ["abba", "beatles"]
            }
        }

        self.assertFalse(event.check_json(content, raises=False))

        content = {
            "person": {
                "attributes": {
                    "hair": "brown",
                    "eye": "green",
                    "skin": "purple"
                },
                "age": 33,
                "fav_books": "nothing",  # should be a list
            }
        }

        self.assertFalse(event.check_json(content, raises=False))


class MockSynapseEvent(SynapseEvent):

    def __init__(self, template):
        self.template = template

    def get_content_template(self):
        return self.template

