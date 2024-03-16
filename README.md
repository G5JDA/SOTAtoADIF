# SOTAtoADIF v1.0.0

Convert SOTA database CSV logs to ADIF. Including enrichment from SOTA API summit data.

Designed for `Python >= 3.10.0, urllib3 >= 2.0.0`.

Specifically intended to produce ADIF files that can be easily uploaded to LoTW using TQSL.
Contrary to what many people seem to believe, **you do not need a station location in TQSL for every single summit!**
As long as you have not changed the default TQSL settings, the locator from the ADIF QSO will be used.
The remaining caveat is your callsign must imply the DXCC entity you operated from.

### ⚠️ Please check the [wiki](https://github.com/G5JDA/SOTAtoADIF/wiki) for important guidance on use with LoTW / TQSL ⚠️

## Author

  - **[Jack G5JDA](https://g5jda.uk)** -
    [GitHub Profile](https://github.com/G5JDA)

See also [acknowledgements](#acknowledgments) and the list of
[contributors](https://github.com/G5JDA/SOTAtoADIF/graphs/contributors)
who participated in this project.

## License

See [LICENSE](LICENSE).

SOTAtoADIF is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SOTAtoADIF is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SOTAtoADIF.
If not, see <https://www.gnu.org/licenses/>.

## Getting Started / How to Use

### Windows

If you know what you're doing with Python on Windows, adapt the Linux guide below.
Otherwise, follow this guide for the simplest approach - note you will only be able to run released versions
(not development or experimental branches). 
If you want to try out upcoming features, or modify the source code, you will have to sacrifice the easy life!

To make your life easy, when releasing a new version of SOTAtoADIF, I use `pyinstaller` to produce a windows `.exe`.
This way you don't need to worry about installing Python or managing a virtual environment.


#### Prerequisites

- An internet connection (both for initial download and use - calls are made to the SOTA API)
- A copy of the latest released `SOTAtoADIF-v*.exe`
  - Download this from GitHub [releases](https://github.com/G5JDA/SOTAtoADIF/releases) (**look in 'Assets' under the newest release**).

#### Use

Open PowerShell (or cmd if you really want).
```shell
# go the directory where you placed the released SOTAtoADIF-v*.exe
cd \path_to_directory_with_exe\

# run SOTAtoADIF (make sure to replace * to match the real filename)
.\SOTAtoADIF-v*.exe <SOTA Database CSV filepath>

# see what options exist
.\SOTAtoADIF-v*.exe -h
```

### Linux

If you are proficient in using Linux, this is probably easier than Windows...

#### Prerequisites

- An internet connection (both for initial download and use - calls are made to the SOTA API).
- `git` - if not present, install with your package manager (e.g. `sudo apt install git`).
- `Python >= 3.10.0` - we will set up a venv.
- `urllib3 >= 2.0.0` - will be automatically installed with our venv creation script.

#### Install
This is linux, we're not really installing a Python script 😉!

However, these steps only need to be followed the first time.
```shell
# clone the repository (no need to grab a specific tag, main branch is stable)
git clone https://github.com/G5JDA/SOTAtoADIF.git

# enter repo directory
cd SOTAtoADIF

# run venv creation script (if this step fails, fix issues then instead follow update section below)
source venv.sh
```

#### Use

Do this each time you want to use SOTAtoADIF.

```shell
# make sure you are in the SOTAtoADIF directory
cd /<path_to>/SOTAtoADIF

# activate the virtual environment
source venv.sh

# run SOTAtoADIF
python3 SOTAtoADIF.py <SOTA Database CSV filepath>

# see what options exist
python3 SOTAtoADIF.py --help
```

#### Update

If it has been a while since you last used SOTAtoADIF, there may be a newer version available.

```shell
# make sure you are in the SOTAtoADIF directory
cd /<path_to>/SOTAtoADIF

# get latest changes from main branch
source update.sh
```


### Mac
If you have a Mac, please feel free to contribute a basic how to use guide.

The steps should be somewhat similar to Linux except you might not already have Python `>=3.10`
and the Bash scripts might not work.

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
1. Install Python `>=3.10`, pip, and Git (or an IDE that provides these).
2. Fork and git clone this repository to your development machine (do not just download the source zip!!).
3. Set up the `venv` for Python (from repo directory in PowerShell or IDE terminal).
   1. `python -m venv .\.venv\`
   2. `.\.venv\Scripts\Activate.ps1`
      1. If this fails with `running scripts is disabled on this system`, run PowerShell 
      as an administrator and execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`
   3. `pip install -r requirements.txt`
4. In future, activate the `venv` in PowerShell with `<repo_path>\.venv\Scripts\Activate.ps1`

## Versioning

This project uses [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/G5JDA/SOTAtoADIF/tags).

## Acknowledgments

  - **[Richard M1HAX](https://m1hax.uk/)** -
    [GitHub Profile](https://github.com/m1hax) -
    Provided first feedback and initial publicity, thanks!

See the list of
[contributors](https://github.com/G5JDA/SOTAtoADIF/graphs/contributors)
who participated in this project.
