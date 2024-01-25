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

import json
import urllib.error
import urllib.request
import urllib3
import warnings

api_url_base = "https://api2.sota.org.uk/api/"


def summit_data_from_ref(summit_ref, http):
    """
    Retrieves summit data from SOTA API
    :param summit_ref: summit reference string, e.g. G/CE-001
    :return: summit data as a dictionary if lookup succeeds, otherwise None
    """
    # return variable - if we don't successfully get the summit data, we return None
    summit_data = None

    # Creating a PoolManager instance for sending requests.
    # http = urllib3.PoolManager()

    try:
        api_url = api_url_base + "summits/" + summit_ref
        # response = urllib.request.urlopen(api_url)
        response = http.request("GET", api_url)
        # status_code = response.getcode()
        status_code = response.status

        match status_code:
            case 200:
                # the good case, we expect api data to be present, decode the json
                # summit_data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
                summit_data = response.json()

            case 204:
                # most likely the summit ref was not found / is invalid
                warnings.warn("\nSOTA API returned status code: " + str(status_code) + ". This means summit reference "
                              + "was not found or is bad. Summit ref: " + summit_ref +
                              ". No enrichment for this summit!")

            case _:
                # some other error with the lookup, unknown
                warnings.warn("\nSOTA API returned status code: " + str(status_code) + ". Unknown error. Summit ref: "
                              + summit_ref + ". No enrichment for this summit!")

    # catch HTTP errors
    except urllib.error.HTTPError as e:
        match e.code:
            case 404:
                # most likely the summit ref is malformed or the API path changed
                warnings.warn("\nSOTA API returned status code: " + str(e.code) +
                              ". Either summit ref is malformed or API has changed. Summit ref: " + summit_ref +
                              ". No enrichment for this summit!")

            case code if code in range(500, 599):
                # some sort of server error
                warnings.warn("\nSOTA API returned status code: " + str(e.code) + ". SOTA API may have changed " +
                              "or is down. Summit ref: " + summit_ref + ". No enrichment for this summit!")

            case _:
                # some other error with the lookup, unknown
                warnings.warn("\nSOTA API returned status code: " + str(e.code) + ". Unknown error. Summit ref: "
                              + summit_ref + ". No enrichment for this summit!")

    # if something went really wrong!
    except (urllib.error.URLError, urllib.error.ContentTooShortError) as e:
        warnings.warn("\nSOTA API Unknown error. Summit ref: " + summit_ref + ". No enrichment for this summit!\n"
                      + "Error info: " + str(e))

    return summit_data
