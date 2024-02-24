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

__version__ = '1.0.0-alpha1'
__author__ = 'Jack G5JDA'

import time
import argparse
import logging
from modules import sota_csv
from modules import sota_api
from modules import adif


if __name__ == '__main__':
    time_start = time.time()  # to measure time taken

    # setup command line arguments and parser
    parser = argparse.ArgumentParser(
        prog='SOTAtoADIF',
        description='Convert SOTA CSV log files to ADIF.',
        epilog='For more information see https://github.com/G5JDA/SOTAtoADIF')

    parser.add_argument('sota_log_path',
                        help='path to SOTA CSV log file (activator/chaser log)')

    parser.add_argument('-c', '--chaser', action='store_true',
                        help='process as a chaser log (changes behaviour of -s)')

    parser.add_argument('-s', '--s2s', metavar='s2s_log_path',
                        help='path to SOTA S2S CSV log file (adds other summit info to output for activator mode, '
                             'removes S2S QSOs in chaser mode)')

    parser.add_argument('-l', '--log', metavar='debug_log_path',
                        help='path to use for SOTAtoADIF debug logging output file, appends, best used with -v'
                             ' (omit to print to console)')

    logging_group = parser.add_mutually_exclusive_group()  # verbose and quiet modes are mutually exclusive

    logging_group.add_argument('-q', '--quiet', action='store_true',
                               help='set log level to WARN (omits informational messages)')

    logging_group.add_argument('-v', '--verbose', action='store_true',
                               help='set log level to DEBUG (maximises information)')

    args = parser.parse_args()

    # setup python logging
    log_level = logging.INFO  # default to INFO level
    log_format = '%(levelname)s: %(message)s'  # default log format

    # modify from default if args specified
    if args.verbose:
        log_level = logging.DEBUG
        log_format = '%(asctime)s | %(levelname)s | %(filename)s (%(lineno)d) | %(funcName)s | %(message)s'
    elif args.quiet:
        log_level = logging.WARN

    # apply logging config
    if args.log:
        logging.basicConfig(filename=args.log, encoding='utf-8', level=log_level, format=log_format)
        logging.info('=*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*=')
        logging.info('=*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*=')
        logging.info('=*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*==*=*=*=*=*=*=*=*=*=*=')
    else:
        logging.basicConfig(level=log_level, format=log_format)

    # start program, end of setup steps
    logging.info('Starting SOTAtoADIF.')
    logging.debug('Log level is: {}'.format(log_level))
    logging.debug('CLI Args: {}'.format(args))

    # temporary bodge for future features
    if args.chaser or args.s2s:
        logging.critical('Options -c -s not yet implemented.')
        exit(1)

    # main program flow
    main_log_path = args.sota_log_path  # get the path to main log file CSV (activator/chaser)
    main_log_rows = sota_csv.read_log(main_log_path)  # read CSV rows into list
    main_log_dict = sota_csv.process_qsos(main_log_rows)  # process rows into QSO dict
    main_log_dict = sota_api.enrich_qsos(main_log_dict)  # enrich QSOs with API data
    adif.output_logs(main_log_dict)  # convert to ADIF and output files

    duration = round(time.time() - time_start, 2)
    logging.info('Completed in {} seconds.'.format(duration))
