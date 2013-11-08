# HockeyStreamsAPI - a Python wrapper for the hockeystreams.com REST API


## Install

- Assumes Python 2.7

    sudo pip install hockeystreams

## Usage

For anonymous access, hockeystreams.com allows the get_scores ability:

    from hockeystreams import HockeyStreams
    hs = HockeyStreams()
    score = hs.get_scores(shouldFilter=True, team="Calgary Flames")[0]
    print "%s: %s"%(score.get_home_team(), score.get_home_score())
    print "%s: %s"%(score.get_away_team(), score.get_away_score())

to determine what fields each returned object has, simply print it out:

    print score

will output something similar to (depending on the api data):

    <Score>
    home_team_city: St Louis
    home_team: St Louis Blues
    away_team: Calgary Flames
    home_team_name: Blues
    tv: None
    period: Final
    short_away_team: CGY
    event: NHL
    home_score: 3
    away_team_name: Flames
    short_home_team: STL
    away_team_city: Calgary
    away_score: 2
    is_playing: 0
    </Score>

from there, each of the models can be accessed as:

    score.get_home_city()
    score.get_short_away_team()
    ...

or

    score.home_city
    score.short_away_team


If you create an account on hockeystreams.com, you can use this wrapper for authenticated access:

    hs = HockeyStreams("cemeyer2", "password")
    on_demand = hs.get_on_demand()[0]
    print on_demand

will output something similar to (depending on the api data):

    <OnDemand>
    home_team: Rouyn-Noranda Huskies
    away_team: Victoriaville Tigres
    id: 12338
    is_wmv: 0
    feed_type:
    date: 11/07/2013
    is_flash: 1
    event: QMJHL
    isi_stream: 1
    </OnDemand>

These objects can be used as the unauthenticated versions.

It is important to note that many of the API functions exposed by hockeystreams.com are only available to
premium members of the site. As such, this wrapper will raise a ValueError if a non-premium account tries to
use any of the API functions which are restricted to premium members. In addition, a ValueError will be raised
if any other error condition arises, with an associated message.

## Contributing

Feel free to fork and improve.

## License 

GPLv2