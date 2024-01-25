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



SOTAtoADIF

This is a program to convert SOTA log CSV files to ADIF format.

In particular, it is intended to be used as part of a workflow
to upload SOTA log files to ARRL LoTW using TQSL.

See README.md or https://github.com/G5JDA/SOTAtoADIF or https://g5jda.uk

Please check CONTRIBUTING.md if you'd like to improve / add to what this program can do.
"""
import time
import argparse

from modules import sota_csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='SOTAtoADIF',
        description='Convert SOTA CSV log files to ADIF.',
        epilog='For more information see https://github.com/G5JDA/SOTAtoADIF')

    parser.add_argument('log_path',
                        help='path to SOTA CSV log file (activator/chaser log)')

    parser.add_argument('-q', '--quiet', action='store_true',
                        help='suppress informational console output')

    parser.add_argument('-c', '--chaser', action='store_true',
                        help='process as a chaser log (changes behaviour of -s)')

    parser.add_argument('-s', '--s2s', metavar='s2s_log_path',
                        help='path to SOTA S2S CSV log file (adds other summit info to output for activator mode, '
                             'removes S2S QSOs in chaser mode)')

    args = parser.parse_args()

    # do stuff
    # data = sota_api.summit_data_from_ref(input("Input summit ref: "))
    # print("Summit locator: " + data.get("locator"))
    file = input("Path to log csv: ")

    t = time.time()
    log = sota_csv.read_log(file)
    t1 = time.time() - t
    t = time.time()
    qsos_r = sota_csv.process_qsos(log)
    t2 = time.time() - t
    t = time.time()
    qsos = sota_csv.enrich_qsos(qsos_r)
    t3 = time.time() - t
    t = time.time()
    print(qsos.keys())
    print('\n\n')
    print(qsos)
    print('\n\n')
    print(t1)
    print(t2)
    print(t3)
