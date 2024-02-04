# SOTAtoADIF v0.1.0

Convert SOTA database CSV logs to ADIF. Including enrichment from SOTA API summit data.

Specifically intended to produce ADIF files that can be easily uploaded to LoTW using TQSL.
Contrary to what many people seem to believe, **you do not need a station location in TQSL for every single summit!**
As long as you have not changed the default TQSL settings, the locator from the ADIF QSO will be used.
The remaining caveat is your callsign must imply the DXCC entity you operated from.

Designed for `Python >= 3.10, urllib3 >= 2`.

## TODO for v1.0.0 release
- [ ] Write basic how to use docs into README
- [ ] Create Wiki on GitHub for more detailed docs - e.g. how to use with TQSL
- [ ] Make big disclaimer / notice that callsign must = single DXCC 
(and CQ/ITU zones but these can be set to NONE if not) otherwise not acceptable for LoTW upload.
  - [ ] maybe also make CLI prompt to agree to this caveat
  - [ ] technically possible to set DXCC to NONE also but then no point uploading to LoTW surely?
- [ ] venv creation script + pip install requirements.txt (python>=3.10, urllib3>=2)

## Ideas / Thoughts

- `Target = v1.0.0`
  - We could use `pyinstaller` to create a less complicated way to use this program for users not familiar with Python.
    - Maybe this is the best option for Windows?
    - Not needed for linux, latest (LTS) releases of major distros are already at least Python 3.10.
    - Mac users can adapt the linux instructions.
- `Target >= v1.1.0`
  - `--quiet (-q)` option.
    - Perhaps also better warning / infomational prints in general.
  - `--ignore-before (-i) [date]` option.
    - Allow users to input full log csv but ignore records before specified date.
    - Otherwise, full log processing and single activation processing are easy, anything inbetween is clumsy.
    - Not so useful for LoTW - TQSL already allows date range selection during import.
- `Target >= v2.0.0`
  - Optional import of S2S CSV, then do some kind of join if all other fields of QSO match, add DX SOTA ref.
    - This has no utility for LoTW so do not include in version 1.
    - Big utility for getting most info from csv into adif - e.g. to import to logging program.
  - Chaser CSV could also be added (not for S2S but will include them without my SOTA ref - a join with S2S could exclude them).
    - Would be better than nothing for adding to logging programs / LoTW for DXCC, but it will be impossible to guess the locator.
    Not an issue for LoTW as long as the station location has blank locator field (docs suggest this is possible, and how 
    LoTW copes with airborne contacts). I guess the user could use their home QTH if they are sure all contacts are from 
    there. Not much gain over ON6ZQ, but I guess worth adding for completeness in version > 1.

## Getting Started / How to Use

Todo

### Prerequisites

- An internet connection (both for initial download and use - calls are made to the SOTA API)
- `Python >= 3.10.0` - use a venv
- `urllib3 >= 2.0.0` - can be installed with pip

### Installing

Todo

### Use

`python3 SOTAtoADIF.py <SOTA Database CSV filepath>`

## Contributing

Essential:
- Develop for Python 3.10.
- Avoid non-standard imports unless you have an undeniable reason:
  - Yes, even if the package can be installed with pip!
  - This is to save ourselves from future dependency chaos.
  - `urllib3` is the only exception so far due to the massive time saving it produces.
- Obey the style guide in [CONTRIBUTING.md](CONTRIBUTING.md)


**If you'd like to contribute a new feature, be sure to create an issue offering to do so first.**
This will likely save much back and forth when compared to surprise PRs!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code
of conduct, and the process for submitting pull requests.

### Installing for Development

#### Linux
1. Fork and git clone this repository to your development machine (do not just download the source zip!!).
2. Follow the `venv` setup instructions for normal users (there are no special requirements for development).

#### Windows
1. Install Python 3.10, pip, and Git (or an IDE that provides these).
2. Fork and git clone this repository to your development machine (do not just download the source zip!!).
3. Set up the `venv` for Python (from repo directory in PowerShell or IDE terminal).
   1. `python -m venv .\venv\`
   2. `pip install -r requirements.txt`
4. In future, activate the `venv` in PowerShell with `<repo_path>\venv\Scripts\Activate.ps1`

## Versioning

This project uses [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/G5JDA/SOTAtoADIF/tags).

## Author

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
