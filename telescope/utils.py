#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2014 Measurement Lab
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

import datetime
import os


class UTC(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


def make_datetime_utc_aware(datetime_timestamp):
    return datetime_timestamp.replace(tzinfo=UTC())


def unix_timestamp_to_utc_datetime(unix_timestamp):
    return datetime.datetime.fromtimestamp(unix_timestamp, tz=UTC())


def build_filename(outpath, date, duration, site, client_provider,
                   client_country, metric, is_affected, suffix):
    """Builds an output filename that reflects the data being written to file.

    Args:
        outpath (str): Indicates the path (excluding filename) where the file
            will be written.
        date (str): A string indicating the start time of the data window the
            file represents.
        duration (str): A string indicating the duration of the data window the
            file represents.
        site (str): The name of the M-Lab site from which the data was collected
            (e.g. lga01)
        client_provider (str): The name of the client provider associated with
            the test results.
        client_country (str): The name of the client country associated with
            the test results.
        metric (str): The name of the metric this data represents (e.g.
            download_throughput).
        is_affected (bool): Whether the test is marked as affected.
        suffix (str): The appended string such as a note on the file information
            or the file extension (e.g. '-bigquery.sql').

    Returns:
       (str): The generated full pathname of the output file.
    """
    filename_format = ("{date}+{duration}_{additional_properties}_"
                       "{metric}-{is_affected}{suffix}")
    additional_properties = "_".join(filter(None, [site, client_country,
                                                   client_provider]))
    is_affected_notation = 'affected' if is_affected else 'not_affected'

    filename = filename_format.format(
        date=date,
        duration=duration,
        additional_properties=additional_properties,
        metric=metric,
        is_affected = is_affected_notation,
        suffix=suffix)
    filename = strip_special_chars(filename)
    filepath = os.path.join(outpath, filename)
    return filepath


def check_for_valid_cache(cache_path, manifest_path=None):
    """Checks for results file previously generated by this tool.

    Args:
        cache_path (str): Built path to cache file that we are interested in.
        manifest_path (str, optional): Built path to cache file that we are
            interested in. Defaults to None.

    Returns:
        bool: True if valid file, False otherwise.
    """
    does_file_exist_at_cache_path = os.path.exists(cache_path)
    return does_file_exist_at_cache_path


def strip_special_chars(filename):
    """Removes shell special characters from a filename.

    Args:
        filename (str): Filename to be sanitized. Note that this should be a
            single filename and not a full path, as this will strip path
            separators.

    Returns:
        (str) Sanitized version of filename.
    """
    sanitized = filename
    special_chars = '\\/"\'`<>|:;\t\n?#$^&*='
    for special_char in special_chars:
        sanitized = sanitized.replace(special_char, '')
    return sanitized


def create_directory_if_not_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name
