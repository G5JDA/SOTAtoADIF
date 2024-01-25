"""
Copyright (c) 2024 Jack G5JDA (https://g5jda.uk)

This file is part of SOTAtoADIF.

SOTAtoADIF is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SOTAtoADIF is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SOTAtoADIF.
If not, see <https://www.gnu.org/licenses/>.



sota_csv.py

Contains functionality needed to make sense of SOTA CSV log files, process them into python dictionaries
"""

import csv
import warnings

import urllib3

from modules import sota_api


def read_log(filepath):
    """
    Reads SOTA CSV log file.
    Specifically no smart processing of the CSV log should be done in this function.
    i.e. we can use this for activator, s2s, chaser, ...? logs without issue
    :param filepath: path to CSV log file
    :return: list of rows from CSV log file (each row itself a list)
    """
    log = []

    # no try-except here: if this doesn't 'just work' we have big problems so dying is probably best
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            log.append(row)

    return log


def process_qsos(raw_log):
    """
    Process SOTA log rows into meaningful QSO records.
    Here we are not aligning the format to ADIF, just reorganising into a structure we prefer.
    :param raw_log: list of rows from SOTA CSV log (output of read_log)
    :return: dictionary of QSO records
    """
    qsos_dict = {}

    # don't try to process an empty log
    if raw_log:
        for record in raw_log:
            match record[0]:
                case 'V2':
                    # the case for normal QSO rows - note some fields may be empty strings ''
                    # note that columns are consistent across activator, s2s, chaser logs (thankfully!)
                    try:
                        qso = {'summit': record[2],
                               'date': record[3],
                               'time': record[4],
                               'frequency': record[5],
                               'mode': record[6],
                               'callsign': record[7],  # this is the callsign of the worked station
                               'other_summit': record[8],  # this is summit of the worked station for s2s/chaser logs
                               'comment': record[9]}

                        # the outer keys in the qsos_dict are callsign used by log owner
                        if record[1] in qsos_dict.keys():
                            # already processed qsos for this callsign, append
                            qsos_dict[record[1]].append(qso)
                        else:
                            # first qso for this callsign, init
                            qsos_dict[record[1]] = [qso]

                    except Exception as e:
                        warnings.warn("\nUnknown error attempting to process log record as QSO. Record skipped: "
                                      + record + "\nError info: " + str(e))

                    continue

                case 'Version':
                    # skip header row present in S2S csv
                    continue

                case '':
                    # skip empty records
                    continue

                case _:
                    # default case means unexpected format
                    warnings.warn("\nUnrecognized version field in CSV row. This could mean the SOTA CSV format has"
                                  + "changed or the CSV file imported is not a SOTA CSV. Skipping row: " + record)
                    continue

    return qsos_dict


def enrich_qsos(qsos_dict):
    """
    Enriches QSOs in the QSO dictionary with locators of 'summit' / 'other_summit' (as applicable).
    Any merging or subtracting of QSOs should occur before enriching to reduce unnecessary API calls.
    :param qsos_dict: Dictionary of QSOs in the format returned by process_qsos()
    :return: qsos_dict enriched with locators where summit refs are successfully looked up in api
    """
    checked_summits_data = {}  # caches all summit data from API (so that each summit ref only requires one API call)
    api_count = 0  # to confirm number of API calls made

    # check input dict is not empty
    if qsos_dict:
        http = urllib3.PoolManager()

        # nested for loops to iterate over every qso
        for callsign in qsos_dict.keys():
            for qso in qsos_dict[callsign]:
                # loop to reuse same code for 'summit' and 'other_summit' lookups
                for key in ['summit', 'other_summit']:
                    summit_type_key = key  # the key of qso dict ('summit' or 'other_summit')
                    summit_ref = qso[summit_type_key]  # local var for summit ref to improve readability

                    # check summit_ref is not blank string
                    if summit_ref:
                        # only make the API call if we do not have a cached copy of the data
                        if summit_ref not in checked_summits_data.keys():
                            summit_data = sota_api.summit_data_from_ref(summit_ref, http)
                            checked_summits_data[summit_ref] = summit_data  # cache the summit data
                            api_count += 1

                        locator_key = summit_type_key + '_locator'  # either 'summit_locator' or 'other_summit_locator'
                        summit_locator = checked_summits_data[summit_ref]['locator']  # get summit locator from cache

                        qso[locator_key] = summit_locator  # we can get away with this since dicts are objects in py

    # TODO quiet mode doesn't print? (or only print in verbose mode???)
    print("Number of unique summits found: " + str(len(checked_summits_data.keys())))
    print("Number of API calls (should equal number of unique summits): " + str(api_count))

    return qsos_dict
