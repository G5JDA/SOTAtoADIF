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
import logging


def read_log(filepath):
    """
    Reads SOTA CSV log file.
    Specifically no smart processing of the CSV log should be done in this function.
    i.e. we can use this for activator, s2s, chaser, ...? logs without issue
    :param filepath: path to CSV log file
    :return: list of rows from CSV log file (each row itself a list)
    """
    log = []
    row_count = 0

    logging.info('Reading SOTA CSV log {}'.format(filepath))

    # no try-except here: if this doesn't 'just work' we have big problems so dying is probably best
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            log.append(row)
            row_count += 1

    logging.info('Read {} rows from {}'.format(row_count, filepath))

    return log


def process_qsos(raw_log):
    """
    Process SOTA log rows into meaningful QSO records.
    Here we are not aligning the format to ADIF, just reorganising into a structure we prefer.
    :param raw_log: list of rows from SOTA CSV log (output of read_log)
    :return: dictionary of QSO records
    """
    qsos_dict = {}

    logging.info('Processing CSV rows into QSOs.')

    # don't try to process an empty log
    if not raw_log:
        logging.debug('raw_log is empty')
        logging.error('No record rows present after loading CSV')
    else:
        for record in raw_log:
            match record[0]:
                case 'V2':
                    # the case for normal QSO rows - note some fields may be empty strings ''
                    # note also that columns are consistent across activator, s2s, chaser logs (thankfully!)
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
                            logging.debug('first QSO found for callsign {}'.format(record[1]))
                            qsos_dict[record[1]] = [qso]

                    except Exception as e:
                        logging.error("\nUnknown error attempting to process log record as QSO. Record skipped: "
                                      + record + "\nError info: " + str(e))

                    continue

                case 'Version':
                    # skip header row present in S2S csv
                    logging.debug('skipping S2S header row')
                    continue

                case '':
                    # skip empty records
                    logging.debug('skipping empty row')
                    continue

                case _:
                    # default case means unexpected format
                    logging.warning("\nUnrecognized version field in CSV row. This could mean the SOTA CSV format has"
                                    + "changed or the CSV file imported is not a SOTA CSV. Skipping row: " + record)
                    continue

    if qsos_dict:
        for key in qsos_dict.keys():
            logging.info('Found {} QSOs with callsign {}.'.format(len(qsos_dict[key]), key))

    return qsos_dict
