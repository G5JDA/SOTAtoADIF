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



sota_api.py

Contains all functionality related to the SOTA API.
e.g. finding summit data from reference
"""

import urllib3
import warnings
from SOTAtoADIF import __version__

# things we need for API calls
api_url_base = "https://api2.sota.org.uk/api/"
user_agent = "Python SOTAtoADIF v{} by G5JDA".format(__version__)
header = {'User-Agent': user_agent}


def summit_data_from_ref(summit_ref):
    """
    Retrieves summit data from SOTA API
    :param summit_ref: summit reference string, e.g. G/CE-001
    :return: summit data as a dictionary if lookup succeeds, otherwise None
    """
    # return variable - if we don't successfully get the summit data, we return None
    summit_data = None

    try:
        api_url = api_url_base + "summits/" + summit_ref
        response = urllib3.request("GET", api_url, retries=3, headers=header)  # using urllib3 global PoolManager
        status_code = response.status

        match status_code:
            case 200:
                # the good case, we expect api data to be present, decode the json
                summit_data = response.json()

            case 204:
                # most likely the summit ref was not found / is invalid
                warnings.warn("\nSOTA API returned status code: " + str(status_code) + ". This means summit reference "
                              + "was not found or is bad. Summit ref: " + summit_ref +
                              ". No enrichment for this summit!")

            case 404:
                # most likely the summit ref is malformed or the API path changed
                warnings.warn("\nSOTA API returned status code: " + str(status_code) +
                              ". Either summit ref is malformed or API has changed. Summit ref: " + summit_ref +
                              ". No enrichment for this summit!")

            case code if code in range(500, 599):
                # some sort of server error
                warnings.warn("\nSOTA API returned status code: " + str(status_code) + ". SOTA API may have changed " +
                              "or is down. Summit ref: " + summit_ref + ". No enrichment for this summit!")

            case _:
                # some other error with the lookup, unknown
                warnings.warn("\nSOTA API returned status code: " + str(status_code) + ". Unknown error. Summit ref: "
                              + summit_ref + ". No enrichment for this summit!")

    # catch urllib3 errors, unfortunately not well documented what's likely to raise the many available
    # we can do better if we get reports of exceptions in the wild
    except Exception as e:
        warnings.warn("\nSOTA API Unknown error. Summit ref: " + summit_ref + ". No enrichment for this summit!\n"
                      + "Error info: " + str(e))

    return summit_data
