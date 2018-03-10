# Archimed Sentinel


Sentinel is an autonomous agent for persisting, processing and automating Archimed V12.1 governance objects and tasks, and for expanded functions in the upcoming Archimed V13 release (Evolution).

Sentinel is implemented as a Python application that binds to a local version 12.1 archimedd instance on each Archimed V12.1 Masternode.

This guide covers installing Sentinel onto an existing 12.1 Masternode in Ubuntu 14.04 / 16.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv

Make sure the local Archimed daemon running is at least version 1.0 (100000)

    $ archimed-cli getinfo | grep version

### 2. Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/ArchimedCoin/Sentiel.git && cd Sentinel
    $ export LC_ALL=C
    $ virtualenv ./venv
    $ ./venv/bin/pip install -r requirements.txt


### 2.a. Check ~/.archimedcore/archimed.conf

Check the configuration setting appending any missing parameters.

    rpcuser=<ADD A RANDOM STRING HERE>
    rpcpassword=<ADD A RANDOM STRING HERE>
    listen=1
    server=1
    discover=1
    rpcport=9012
    rpcthreads=8
    rpcallowip=127.0.0.1
    daemon=1
    staking=0


### 2.b. remove old files
Enter the wallet folder and stop the wallet

    archimed-cli stop

Enter the archimed config folder mentioned during the installation

    cd ~/.archimedcore
    rm mncache.dat
    rm mnpayments.dat

Enter the wallet folder and restart the wallet

    archimedd -daemon -reindex

Check the sync status

    watch archimed-cli mnsync status

As soon as you see the following response press CTRL+C

    archimed-cli mnsync status
    {
    "AssetID": 999,
    "AssetName": "MASTERNODE_SYNC_FINISHED",
    "Attempt": 0,
    "IsBlockchainSynced": true,
    "IsMasternodeListSynced": true,
    "IsWinnersListSynced": true,
    "IsSynced": true,
    "IsFailed": false
    }

Finally start the masternode

    archimed-cli masternode start


### 3. Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/home/YOURUSERNAME/sentinel' to the path where you cloned sentinel to:

    * * * * * cd /home/YOURUSERNAME/Sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### 4. Test the Configuration

Test the config by runnings all tests from the sentinel folder you cloned into

    $ cd ~/sentinelLinux && ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with archimedd and the installation is complete

## Configuration

An alternative (non-default) path to the `archimed.conf` file can be specified in `sentinel.conf`:

    archimed_conf=/path/to/archimed.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ cd ~/Sentinel && SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

## Contributing

Specifically:


    To contribute a patch, the workflow is as follows:

    * Fork repository
    * Create topic branch
    * Commit patches

    In general commits should be atomic and diffs should be easy to read. For this reason do not mix any formatting fixes or code moves with actual code changes.

    Commit messages should be verbose by default, consisting of a short subject line (50 chars max), a blank line and detailed explanatory text as separate paragraph(s); unless the title alone is self-explanatory (like "Corrected typo in main.cpp") then a single title line is sufficient. Commit messages should be helpful to people reading your code in the future, so explain the reasoning for your decisions. Further explanation [here](http://chris.beams.io/posts/git-commit/).

### License

Released under the MIT license, under the same terms as ArchimedCore itself. See [LICENSE](LICENSE) for more info.
