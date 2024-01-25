# SOTAtoADIF v0.1.0

Convert SOTA database CSV logs to ADIF. Including enrichment from SOTA API summit data.

Specifically intended to produce ADIF files that can be easily uploaded to LoTW using TQSL.
Contrary to what many people seem to believe, you do not need a station location in TQSL for every single summit!
As long as you have not changed the default TQSL settings, the locator from the ADIF QSO will be used.
The remaining caveat is your callsign must imply the DXCC entity you operated from.

Designed to work with only default python packages to prevent future dependency issues.

## Pseudocode
- [x] Read activator CSV
  - [x] For each line, add QSO to dict (first key is station callsign)
- [ ] S2S enrichment would happen here
- [x] For each QSO in dict
  - [x] look up sota-ref to get locator (keep record of looked up refs in this run to reduce API queries)
- [ ] For each station callsign in dict
  - [ ] Generate ADIF header string, append to ADIF string
  - [ ] For each QSO in array
    - [ ] Generate QSO ADIF string, append to ADIF string
    - [ ] convert MHz to band
    - [ ] convert mode to adif mode (and sub-mode if relevant)
  - [ ] Generate ADIF footer (if such a thing), append to ADIF string
  - [ ] Write ADIF file for station callsign

## TODO
- [ ] Squash all commits and force push to main
- [ ] Write basic how to use docs into README
- [ ] Add proper error handling so user feedback is useful
- [ ] Create Wiki on GitHub for more detailed docs
- [ ] Make big disclaimer / notice that callsign must = single DXCC 
(and CQ/ITU zones but these can be set to NONE if not) otherwise not acceptable for LoTW upload.
  - [ ] maybe also make CLI prompt to agree to this caveat
  - [ ] technically possible to set DXCC to NONE also but then no point uploading to LoTW surely?

## Ideas / Thoughts

- [ ] Optional import of S2S CSV, then do some kind of join if all other fields of QSO match, add DX SOTA ref
  - This has no utility for LoTW so do not include in version 1
  - Big utility for getting most info from csv into adif - e.g. to import to logging program
- [ ] Chaser CSV could also be added (not for S2S but will include them without my SOTA ref - a join with S2S could exclude them)
  - Would be better than nothing for adding to logging programs / LoTW for DXCC, but it will be impossible to guess the locator.
  Not an issue for LoTW as long as the station location has blank locator field (docs suggest this is possible, and how 
  LoTW copes with airborne contacts). I guess the user could use their home QTH if they are sure all contacts are from 
  there. Not much gain over ON6ZQ, but I guess worth adding for completeness in version > 1.
- [ ] Should we allow non-default included modules just so we can use urllib3?
  - This may significantly speed up the API lookups as built-in urllib 
  reestablishes a connection for each request (including DNS lookup!!!)
  SOTA API is https only so overhead is quite high.
- [ ] We could use pyinstaller to create a less complicated way to use this program for users not familiar with python

## Getting Started / How to Use

Todo

### Prerequisites

- An internet connection (both for initial download and use - calls are made to the SOTA API)
- A Python installation on your computer (version 3.10 or greater required, 3.12 used for development)

### Installing

Todo

## Contributing

Essential:
- Develop for no older than Python 3.10, preferably 3.11 or 3.12.
- Do not require non-standard imports (yes, even if the package can be installed with pip!)

If you'd like to contribute a new feature, be sure to create an issue offering to do so first.
This will likely save much back and forth when compared to surprise PRs!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code
of conduct, and the process for submitting pull requests.

## Versioning

This project uses [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/G5JDA/SOTAtoADIF/tags).

## Authors

  - **[Jack G5JDA](https://g5jda.uk)** -
    [GitHub Profile](https://github.com/G5JDA)

See also the list of
[contributors](https://github.com/G5JDA/SOTAtoADIF/graphs/contributors)
who participated in this project.

## License

SOTAtoADIF is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SOTAtoADIF is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SOTAtoADIF.
If not, see <https://www.gnu.org/licenses/>.

## Acknowledgments

  - TODO
