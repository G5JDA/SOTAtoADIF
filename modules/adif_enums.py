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

# dictionary to hold the chaos that is ADIF mode enumeration
_modes_dict = {
    "AM": None,
    "ARDOP": None,
    "ATV": None,
    "CHIP": ["CHIP64", "CHIP128"],
    "CLO": None,
    "CONTESTI": None,
    "CW": ["PCW"],
    "DIGITALVOICE": ["C4FM", "DMR", "DSTAR", "FREEDV", "M17"],
    "DOMINO": ["DOM-M", "DOM4", "DOM5", "DOM8", "DOM11", "DOM16", "DOM22", "DOM44", "DOM88", "DOMINOEX", "DOMINOF"],
    "DYNAMIC": ["VARA HF", "VARA SATELLITE", "VARA FM 1200", "VARA FM 9600"],
    "FAX": None,
    "FM": None,
    "FSK441": None,
    "FT8": None,
    "HELL": ["FMHELL", "FSKHELL", "HELL80", "HELLX5", "HELLX9", "HFSK", "PSKHELL", "SLOWHELL"],
    "ISCAT": ["ISCAT-A", "ISCAT-B"],
    "JT4": ["JT4A", "JT4B", "JT4C", "JT4D", "JT4E", "JT4F", "JT4G"],
    "JT6M": None,
    "JT9": ["JT9-1", "JT9-2", "JT9-5", "JT9-10", "JT9-30", "JT9A", "JT9B", "JT9C", "JT9D", "JT9E", "JT9E FAST", "JT9F",
            "JT9F FAST", "JT9G", "JT9G FAST", "JT9H", "JT9H FAST"],
    "JT44": None,
    "JT65": ["JT65A", "JT65B", "JT65B2", "JT65C", "JT65C2"],
    "MFSK": ["FSQCALL", "FST4", "FST4W", "FT4", "JS8", "JTMS", "MFSK4", "MFSK8", "MFSK11", "MFSK16", "MFSK22", "MFSK31",
             "MFSK32", "MFSK64", "MFSK64L", "MFSK128", "MFSK128L", "Q65"],
    "MSK144": None,
    "MT63": None,
    "OLIVIA": ["OLIVIA 4/125", "OLIVIA 4/250", "OLIVIA 8/250", "OLIVIA 8/500", "OLIVIA 16/500", "OLIVIA 16/1000",
               "OLIVIA 32/1000"],
    "OPERA": ["OPERA-BEACON", "OPERA-QSO"],
    "PAC": ["PAC2", "PAC3", "PAC4"],
    "PAX": ["PAX2"],
    "PKT": None,
    "PSK": ["8PSK125", "8PSK125F", "8PSK125FL", "8PSK250", "8PSK250F", "8PSK250FL", "8PSK500", "8PSK500F", "8PSK1000",
            "8PSK1000F", "8PSK1200F", "FSK31", "PSK10", "PSK31", "PSK63", "PSK63F", "PSK63RC4", "PSK63RC5", "PSK63RC10",
            "PSK63RC20", "PSK63RC32", "PSK125", "PSK125C12", "PSK125R", "PSK125RC10", "PSK125RC12", "PSK125RC16",
            "PSK125RC4", "PSK125RC5", "PSK250", "PSK250C6", "PSK250R", "PSK250RC2", "PSK250RC3", "PSK250RC5",
            "PSK250RC6", "PSK250RC7", "PSK500", "PSK500C2", "PSK500C4", "PSK500R", "PSK500RC2", "PSK500RC3",
            "PSK500RC4", "PSK800C2", "PSK800RC2", "PSK1000", "PSK1000C2", "PSK1000R", "PSK1000RC2", "PSKAM10",
            "PSKAM31", "PSKAM50", "PSKFEC31", "QPSK31", "QPSK63", "QPSK125", "QPSK250", "QPSK500", "SIM31"],
    "PSK2K": None,
    "Q15": None,
    "QRA64": ["QRA64A", "QRA64B", "QRA64C", "QRA64D", "QRA64E"],
    "ROS": ["ROS-EME", "ROS-HF", "ROS-MF"],
    "RTTY": ["ASCI"],
    "RTTYM": None,
    "SSB": ["LSB", "USB"],
    "SSTV": None,
    "T10": None,
    "THOR": ["THOR-M", "THOR4", "THOR5", "THOR8", "THOR11", "THOR16", "THOR22", "THOR25X4", "THOR50X1", "THOR50X2",
             "THOR100"],
    "THRB": ["THRBX", "THRBX1", "THRBX2", "THRBX4", "THROB1", "THROB2", "THROB4"],
    "TOR": ["AMTORFEC", "GTOR", "NAVTEX", "SITORB"],
    "V4": None,
    "VOI": None,
    "WINMOR": None,
    "WSPR": None
}


def enum_mode(mode_string):
    """
    Enumerate the mode to ADIF spec
    :param mode_string: mode string to enumerate
    :return: {'mode': '', 'sub-mode': ''} e.g. {'mode': 'SSB', 'sub-mode': 'LSB'}
    """
    mode_string = mode_string.upper()
    sub_mode_string = None

    # not entering this if block means the mode is a top level ADIF mode, skip straight to the return
    if mode_string not in _modes_dict.keys():
        # iterate over modes in dict
        for mode in _modes_dict.keys():
            sub_modes = _modes_dict[mode]
            # catch no sub-modes
            if sub_modes:
                if mode_string in sub_modes:
                    # the string input to this function matches a sub-mode
                    sub_mode_string = mode_string  # move the input to sub-mode
                    mode_string = mode  # set mode to key of list sub-mode was found in
                    break  # stop iterating over modes dict

        if not sub_mode_string:
            # we have iterated over all sub-modes and still not found a match!
            message = '\nMode not a valid ADIF mode, program importing ADIF will probably complain.'
            message += ' Please report this in a Github issue: '
            message += mode_string
            warnings.warn(message)

    return {'mode': mode_string, 'sub_mode': sub_mode_string}


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
        message = '\nFrequency string does not end with Hz. Please report this in a Github issue: ' + str(frequency)
        warnings.warn(message)

    return band
