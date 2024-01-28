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



adif_enums.py

Handles conversion of data to ADIF specified enums which are in effect strings
"""

import warnings


def frequency_to_band(frequency):
    """
    Converts a frequency string to a band string as defined in ADIF spec
    :param frequency: Frequency string e.g. '144MHz'
    :return: Band string e.g. '2m', empty if unsuccessful i.e. ''
    """
    band = ''  # band string to return, if not successful return empty string

    if frequency.endswith('Hz'):
        # format is probably what we expect
        frequency = frequency.removesuffix('Hz')

        if frequency.endswith('M'):
            # this is the only case observed so far in wild SOTA CSVs
            frequency = frequency.removesuffix('M')  # at this point we should be left with the numeric part only
            float_frequency = float(frequency)

            # let's support every band in the ADIF spec! (2190m SOTA someone?)
            match float_frequency:
                case freq if (0.1357 <= freq <= 0.1378):
                    band = '2190m'
                case freq if (0.472 <= freq <= 0.479):
                    band = '630m'
                case freq if (0.501 <= freq <= 0.504):
                    band = '560m'
                case freq if (1.8 <= freq <= 2.0):
                    band = '160m'
                case freq if (3.5 <= freq <= 4.0):
                    band = '80m'
                case freq if (5.0 <= freq < 5.06):
                    # this is outside the ADIF spec but predicted to be an issue based on SOTA CSV
                    band = '60m'
                case freq if (5.06 <= freq <= 5.45):
                    band = '60m'
                case freq if (7.0 <= freq <= 7.3):
                    band = '40m'
                case freq if (10.0 <= freq < 10.1):
                    # this is outside the ADIF spec but predicted to be an issue based on SOTA CSV
                    band = '30m'
                case freq if (10.1 <= freq <= 10.15):
                    band = '30m'
                case freq if (14.0 <= freq <= 14.35):
                    band = '20m'
                case freq if (18.0 <= freq < 18.068):
                    # this is outside the ADIF spec but predicted to be an issue based on SOTA CSV
                    band = '17m'
                case freq if (18.068 <= freq <= 18.168):
                    band = '17m'
                case freq if (21.0 <= freq <= 21.45):
                    band = '15m'
                case freq if (24.0 <= freq < 24.89):
                    # this is outside the ADIF spec but predicted to be an issue based on SOTA CSV
                    band = '12m'
                case freq if (24.89 <= freq <= 24.99):
                    band = '12m'
                case freq if (28.0 <= freq <= 29.7):
                    band = '10m'
                case freq if (40.0 <= freq <= 45.0):
                    band = '8m'
                case freq if (50.0 <= freq <= 54.0):
                    band = '6m'
                case freq if (54.000001 <= freq <= 69.9):
                    band = '5m'
                case freq if (70.0 <= freq <= 71.0):
                    band = '4m'
                case freq if (144.0 <= freq <= 148.0):
                    band = '2m'
                case freq if (222.0 <= freq <= 225.0):
                    band = '1.25m'
                case freq if (420.0 <= freq <= 450.0):
                    band = '70cm'
                case freq if (902.0 <= freq <= 928.0):
                    band = '33cm'
                case freq if (1240.0 <= freq <= 1300.0):
                    band = '23cm'
                case freq if (2300.0 <= freq <= 2450.0):
                    band = '13cm'
                case freq if (3300.0 <= freq <= 3500.0):
                    band = '9cm'
                case freq if (5650.0 <= freq <= 5925.0):
                    band = '6cm'
                case freq if (10000.0 <= freq <= 10500.0):
                    band = '3cm'
                case freq if (24000.0 <= freq <= 24250.0):
                    band = '1.25cm'
                case freq if (47000.0 <= freq <= 47200.0):
                    band = '6mm'
                case freq if (75500.0 <= freq <= 81000.0):
                    band = '4mm'
                case freq if (119980.0 <= freq <= 123000.0):
                    band = '2.5mm'
                case freq if (134000.0 <= freq <= 149000.0):
                    band = '2mm'
                case freq if (241000.0 <= freq <= 250000.0):
                    band = '1mm'
                case freq if (300000.0 <= freq <= 7500000.0):
                    band = 'submm'
                case _:
                    message = '\nFrequency MHz value not in ADIF specification. Please report this in a Github issue: '
                    message += str(frequency)
                    warnings.warn(message)

        else:
            message = '\nFrequency string uses an SI prefix other than Mega. Please report this in a Github issue: '
            message += str(frequency)
            warnings.warn(message)

    else:
        warnings.warn('\nFrequency string does not end with Hz, cannot convert to ADIF band: {}'.format(frequency))

    return band

# TODO mode string to ADIF mode (and sub-mode) - this is going to be nasty!
