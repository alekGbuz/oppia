# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common utility functions."""

__author__ = 'sll@google.com (Sean Lip)'

import copy
import os
import random
import unicodedata
import yaml

import feconf


class InvalidInputException(Exception):
    """Error class for invalid input."""
    pass


class EntityIdNotFoundError(Exception):
    """Error class for when an entity ID is not in the datastore."""
    pass


class ValidationError(Exception):
    """Error class for when a domain object fails validation."""
    pass


def create_enum(*sequential, **names):
    enums = dict(zip(sequential, sequential), **names)
    return type('Enum', (), enums)


def get_file_contents(filepath, raw_bytes=False):
    """Gets the contents of a file, given a relative filepath from oppia/."""
    with open(filepath) as f:
        return f.read() if raw_bytes else f.read().decode('utf-8')


def get_sample_exploration_yaml(filename):
    """Gets the content of [filename].yaml in the sample explorations folder."""
    return get_file_contents(
        os.path.join(feconf.SAMPLE_EXPLORATIONS_DIR, '%s.yaml' % filename))


def get_comma_sep_string_from_list(items):
    """Turns a list of items into a comma-separated string."""

    if not items:
        return ''

    if len(items) == 1:
        return items[0]

    return '%s and %s' % (', '.join(items[:-1]), items[-1])


def to_ascii(string):
    """Change unicode characters in a string to ascii if possible."""
    return unicodedata.normalize(
        'NFKD', unicode(string)).encode('ascii', 'ignore')


def yaml_from_dict(dictionary):
    """Gets the YAML representation of a dict."""
    return yaml.safe_dump(dictionary, default_flow_style=False)


def dict_from_yaml(yaml_file):
    """Gets the dict representation of a YAML file."""
    try:
        yaml_dict = yaml.safe_load(yaml_file)
        assert isinstance(yaml_dict, dict)
        return yaml_dict
    except yaml.YAMLError as e:
        raise InvalidInputException(e)


def recursively_remove_key(d, key_to_remove):
    """Recursively removes keys from a dict."""
    if isinstance(d, list):
        for item in d:
            recursively_remove_key(item, key_to_remove)
    elif isinstance(d, dict):
        if key_to_remove in d:
            del d[key_to_remove]
        for key, unused_value in d.items():
            recursively_remove_key(d[key], key_to_remove)


def get_random_int(upper_bound):
    """Returns a random integer in [0, upper_bound)."""
    assert upper_bound >= 0 and isinstance(upper_bound, int)

    generator = random.SystemRandom()
    return generator.randrange(0, upper_bound)


def get_random_choice(alist):
    """Gets a random element from a list."""
    assert isinstance(alist, list) and len(alist) > 0

    index = get_random_int(len(alist))
    return alist[index]
