__author__ = 'Charlie Meyer'

from os.path import exists, join, expanduser, realpath
import sys, os, urllib, urllib2, json, traceback
from pprint import pprint


class HSUtil:

    class __impl:
        def get_api_key(self):
            return "1f160e46fba7aec26a6ac5b82a6ffc2f"

        def get_json(self, url, params):
            return self.__json(url, params, 'GET')

        def post_json(self, url, params):
            return self.__json(url, params, 'POST')

        def __json(self, url, params, type):
            try:
                if type == 'GET':
                    url = "".join([url,params])
                request = urllib2.Request(url)
                request.add_header('content-type', 'application/x-www-form-urlencoded')
                response = None
                if type == 'GET':
                    response = urllib2.urlopen(request)
                else:
                    response = urllib2.urlopen(request, params)
                page = response.read()
                code = response.code
                response.close()
                if code == 204:
                    return {}
                js = json.loads(page)
                self.__error_parse(js)
                return js

            except urllib2.HTTPError as e:
                if e.getcode() == 400:
                    self.__error_parse(json.loads(e.read()))
                else:
                    print "unknown http error, code="+e.getcode()
                sys.exit(1)

        def __error_parse(self, js):
            if type(js) == list:
                return
            if js.has_key('status') and str(js['status']) == 'Failed':
                print js['msg']
                sys.exit(1)

        def __base_url(self):
            return 'https://api.hockeystreams.com/'

        def __ep(self, ep):
            return "".join([self.__base_url(), ep])

        def get_scores_endpoint(self, endpoint = 'Scores?'):
            return self.__ep(endpoint)

        def get_login_endpoint(self, endpoint = 'Login?'):
            return self.__ep(endpoint)

        def get_get_live_endpoint(self, endpoint = 'GetLive?'):
            return self.__ep(endpoint)

        def get_live_stream_endpoint(self, endpoint = 'GetLiveStream?'):
            return self.__ep(endpoint)

        def get_on_demand_dates_endpoint(self, endpoint = 'GetOnDemandDates?'):
            return self.__ep(endpoint)

        def get_on_demand_endpoint(self, endpoint = 'GetOnDemand?'):
            return self.__ep(endpoint)

        def get_on_demand_stream_endpoint(self, endpoint = 'GetOnDemandStream?'):
            return self.__ep(endpoint)

        def get_highlights_endpoint(self, endpoint = 'GetHighlights?'):
            return self.__ep(endpoint)

        def get_ip_exception_endpoint(self, endpoint = 'IPException?'):
            return self.__ep(endpoint)

        def get_condensed_games_endpoint(self, endpoint = 'GetCondensedGames?'):
            return self.__ep(endpoint)

        def get_list_teams_endpoint(self, endpoint = 'ListTeams?'):
            return self.__ep(endpoint)

        def get_locations_endpoint(self, endpoint= 'GetLocations?'):
            return self.__ep(endpoint)

    __instance = None

    def __init__(self):
        if HSUtil.__instance is None:
            HSUtil.__instance = HSUtil.__impl()
        self.__dict__['_Singleton__instance'] = HSUtil.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

class HockeyStreams:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.util = HSUtil()
        self.__login()
        self.ip_exception()

    def __login(self):
        data = urllib.urlencode({
            'username': self.username,
            'password': self.password,
            'key': self.util.get_api_key()
        })
        js = self.util.post_json(self.util.get_login_endpoint(), data)
        if str(js['status']) != 'Success':
            print "Login failed"
            sys.exit(1)

        self.uid = js['uid']
        self.favorite_team = js['favteam']
        self.token = js['token']
        self.membership = js['membership']

    def get_favorite_team(self):
        return self.favorite_team

    def get_membership(self):
        return self.membership

    def __get_token(self):
        return self.token

    def get_uid(self):
        return self.uid

    def get_username(self):
        return self.username

    #date should be str MM/DD/YYYY, none for today
    def get_live(self, shouldFilter = False, team = None, date=None):
        if team is None:
            team = self.get_favorite_team()
        params = {'token': self.__get_token()}
        if date is not None:
            params['date'] = date;
        data = urllib.urlencode(params)
        js = self.util.get_json(self.util.get_get_live_endpoint(), data)
        live_list = js['schedule']
        if shouldFilter:
            live_list = self.__filter_team(live_list, team)
        return live_list

    def get_scores(self, shouldFilter = False, team = None):
        if team is None:
            team = self.get_favorite_team()
        #dont mind making this one public since anyone can make one
        data = urllib.urlencode({
            'key': 'ba74e5be0488146301152af4cb0dd23d'
        })
        js = self.util.get_json(self.util.get_scores_endpoint(), data)
        scores_list = js['scores']
        if shouldFilter:
            scores_list = self.__filter_team(scores_list, team)
        return scores_list

    def __filter_team(self, objs, team):
        def filterf(obj):
            if obj.has_key('homeTeam') and str(obj['homeTeam']) == team:
                return True
            if obj.has_key('awayTeam') and str(obj['awayTeam']) == team:
                return True
            return False
        return filter(filterf, objs)

    def extract_score(self, obj, team = None):
        if team is None:
            team = self.get_favorite_team()
        if obj.has_key('homeScore'):
            return int(obj['homeScore'])
        if obj.has_key('awayScore'):
            return int(obj['awayScore'])

    def ip_exception(self):
        data = urllib.urlencode({
            'token': self.__get_token()
        })
        js = self.util.post_json(self.util.get_ip_exception_endpoint(), data)
        if str(js['status']) == 'Success':
            return True
        return False

    def get_live_stream(self, stream_id, location=None):
        params = {}
        params['token'] = self.__get_token()
        params['id'] = int(stream_id)
        if location is not None:
            params['location'] = location
        data = urllib.urlencode(params)
        js = self.util.get_json(self.util.get_live_stream_endpoint(), data)
        return js

    def get_locations(self):
        return self.util.get_json(self.util.get_locations_endpoint(), "")

    def get_on_demand_dates(self):
        data = urllib.urlencode({
            'token': self.__get_token()
        })
        return self.util.get_json(self.util.get_on_demand_dates_endpoint(), data)['dates']

    def get_on_demand(self, date=None, team=None):
        params = {'token': self.__get_token()}
        if date is not None:
            params['date'] = date
        if team is not None:
            params['team'] = team
        data = urllib.urlencode(params)
        return self.util.get_json(self.util.get_on_demand_endpoint(), data)['ondemand']

