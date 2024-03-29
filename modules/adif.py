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



adif.py

Handles production of ADIF format including output of files
"""

import logging
from datetime import datetime, timezone
from modules import adif_enums
from SOTAtoADIF import __version__


def generate_header(callsign, now):
    """
    Generates an ADIF header for a given callsign
    :param now: datetime object in UTC with zeroed microseconds
    :param callsign: station callsign as string
    :return: ADIF header as string (this includes a comment as the first two lines & newline at the end)
    """
    logging.debug("Generating ADIF header for callsign {}".format(callsign))

    now_adif = now.strftime("%Y%m%d %H%M%S")  # convert to the weird ADIF timestamp format
    now_comment = now.strftime("%Y-%m-%d %H:%M:%S")

    header = "# Generated by SOTAtoADIF v{} at {} UTC for {}.\n".format(__version__, now_comment, callsign)
    header += "# SOTAtoADIF is an open-source program authored by G5JDA and licensed under the GNU GPL v3+ license.\n"
    header += "# See https://github.com/G5JDA/SOTAtoADIF or https://g5jda.uk for more info.\n"
    header += "<ADIF_VER:5>3.1.4\n"
    header += "<PROGRAMID:10>SOTAtoADIF\n"
    header += "<PROGRAMVERSION:{}>{}\n".format(len(__version__), __version__)
    header += "<CREATED_TIMESTAMP:{}>{}\n".format(len(now_adif), now_adif)
    header += "<EOH>\n"

    return header


def generate_qsos(station_callsign, qso_list):
    """
    Generate ADIF format string containing QSOs
    :param station_callsign: callsign of the logger's station
    :param qso_list: list of QSOs
    :return: string containing QSOs in ADIF record format
    """
    qsos_adif = ''

    logging.debug("Generating ADIF QSO records for callsign {}".format(station_callsign))

    for qso in qso_list:
        # conversions to ADIF enums / formats
        band = adif_enums.frequency_to_band(qso['frequency'])
        modes = adif_enums.enum_mode(qso['mode'])
        mode = modes['mode']
        sub_mode = modes['sub_mode']
        time = qso['time'].replace(":", "")
        date_parts = qso['date'].split("/")
        date = str(date_parts[2]) + str(date_parts[1]) + str(date_parts[0])

        # assemble ADIF QSO string
        qso_adif = "<CALL:{}>{}".format(len(qso['callsign']), qso['callsign'])
        qso_adif += "<STATION_CALLSIGN:{}>{}".format(len(station_callsign), station_callsign)
        qso_adif += "<QSO_DATE:{}>{}".format(len(date), date)
        qso_adif += "<TIME_ON:{}>{}".format(len(time), time)

        if mode:
            qso_adif += "<MODE:{}>{}".format(len(mode), mode)

        if sub_mode:
            qso_adif += "<SUBMODE:{}>{}".format(len(sub_mode), sub_mode)

        if band:
            qso_adif += "<BAND:{}>{}".format(len(band), band)
        else:
            message = "\nNot outputting QSO since band lookup failed."
            message += " Callsign: {}. QSO: {}.".format(station_callsign, str(qso))
            logging.warning(message)
            continue  # skip this QSO

        if qso.get('summit', None):
            qso_adif += "<MY_SOTA_REF:{}>{}".format(len(qso['summit']), qso['summit'])

        if qso.get('summit_locator', None):
            # TODO this is wrong in chaser mode, should become gridsquare
            qso_adif += "<MY_GRIDSQUARE:{}>{}".format(len(qso['summit_locator']), qso['summit_locator'])
        else:
            # TODO skip this warning in chaser mode, we expect to have no grid
            message = "\nNot outputting QSO since my_gridsquare is missing and not using chaser mode."
            message += " Callsign: {}. QSO: {}.".format(station_callsign, str(qso))
            logging.warning(message)
            continue  # skip this QSO

        if qso.get('other_summit', None):
            qso_adif += "<MY_SOTA_REF:{}>{}".format(len(qso['other_summit']), qso['other_summit'])

        if qso.get('other_summit_locator', None):
            # TODO this is wrong in chaser mode, should become my_gridsquare
            qso_adif += "<GRIDSQUARE:{}>{}".format(len(qso['other_summit_locator']), qso['other_summit_locator'])

        # construct comment
        # TODO this is wrong in chaser mode
        comment = ''
        if qso.get('summit', None):
            comment += "My SOTA Ref: {}.".format(qso['summit'])
        if qso.get('other_summit', None):
            comment += " THX S2S, Your SOTA Ref: {}.".format(qso['summit'])
        if qso.get('comment', None):
            comment += " "
            comment += qso['comment']
        if comment:
            qso_adif += "<COMMENT:{}>{}".format(len(comment), comment)

        qso_adif += '<EOR>\n'  # end of QSO record
        qsos_adif += qso_adif  # add this QSO to the end of the full ADIF QSOs string

    return qsos_adif


def write_adi(adi_string, callsign, now):
    """
    Write the ADIF string to file
    :param adi_string: ADIF formatted string, content for output to file
    :param callsign: Callsign for filename generation
    :param now: Datetime for filename generation
    """
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "{}_SOTAtoADIF_{}.adi".format(callsign, timestamp)
    filename = filename.replace('/', '-')

    logging.info("Writing ADIF to {}".format(filename))

    with open(filename, 'x') as f:
        f.write(adi_string)


def output_logs(log_dict):
    """
    Write out the logs to ADIF files
    :param log_dict: dict in format output by sota_csv.process_qsos()
    :return: Number of files written
    """
    now = datetime.now(timezone.utc).replace(microsecond=0)  # UTC time now (microseconds are unnecessary)
    written_count = 0

    logging.info("Preparing ADIF for output.")

    # only operate on non-empty input
    if not log_dict:
        logging.debug("log_dict is empty")
        logging.warning("There are no logs to output.")
    else:
        # loop over station callsigns (this results in one file output per station callsign in log dict)
        for callsign in log_dict.keys():
            logging.debug("Preparing ADIF for {}".format(callsign))

            # only output a file for this callsign if there are QSOs present
            if log_dict[callsign]:
                adif_string = generate_header(callsign, now)  # prepare ADIF string with ADIF header
                adif_string += generate_qsos(callsign, log_dict[callsign])  # add the QSO records
                write_adi(adif_string, callsign, now)  # write the .adi
                written_count += 1
            else:
                logging.debug('log_dict[callsign] is empty')
                message = "\nNot outputting file for {} since no QSOs present in processed dict.".format(callsign)
                message += " No QSOs were successfully prepared for output for this callsign."
                logging.warning(message)

    logging.info("Wrote {} ADIF log files.".format(written_count))

    return written_count
