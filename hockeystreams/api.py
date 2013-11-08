__author__ = 'Charlie Meyer <charlie@charliemeyer.net>'

import sys, urllib, models, hsutil

class HockeyStreams:

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.util = hsutil.HSUtil()
        self.uid = None
        self.favorite_team = None
        self.token = None
        self.membership = None
        if username is not None and password is not None:
            self.__login()

    def is_logged_in(self):
        return self.uid is not None

    def __login(self):
        data = urllib.urlencode({
            'username': self.username,
            'password': self.password,
            'key': self.util.get_api_key()
        })
        js = self.util.post_json(self.util.get_login_endpoint(), data)
        if str(js['status']) != 'Success':
            raise ValueError("Login failed")
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

    def is_premium(self):
        membership = self.get_membership()
        return membership is not None and membership == "Premium"

    def __check_premium(self):
        self.__check_logged_in()
        if not self.is_premium():
            raise ValueError("Not a premium member")

    def __check_logged_in(self):
        if not self.is_logged_in():
            raise ValueError("Not logged into hockeystreams.com")

    #date should be str MM/DD/YYYY, none for today
    def get_live_streams(self, shouldFilter = False, team = None, date=None):
        self.__check_premium()
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
        return self.util.json_to_objs(live_list, models.LiveStream)

    def get_scores(self, shouldFilter = False, team = None):
        if team is None and self.get_favorite_team() is not None:
            team = self.get_favorite_team()
        #dont mind putting this one here since it is the only endpoint that uses it
        data = urllib.urlencode({
            'key': 'ba74e5be0488146301152af4cb0dd23d'
        })
        js = self.util.get_json(self.util.get_scores_endpoint(), data)
        scores_list = js['scores']
        if shouldFilter and team is not None:
            scores_list = self.__filter_team(scores_list, team)
        return self.util.json_to_objs(scores_list, models.Score)

    def __filter_team(self, objs, team):
        def filterf(obj):
            if obj.has_key('homeTeam') and str(obj['homeTeam']) == team:
                return True
            if obj.has_key('awayTeam') and str(obj['awayTeam']) == team:
                return True
            return False
        return filter(filterf, objs)

    def ip_exception(self):
        self.__check_premium()
        data = urllib.urlencode({
            'token': self.__get_token()
        })
        js = self.util.post_json(self.util.get_ip_exception_endpoint(), data)
        if str(js['status']) == 'Success':
            return True
        return False

    def get_live_stream(self, stream_id, location=None):
        self.__check_premium()
        params = {}
        params['token'] = self.__get_token()
        params['id'] = int(stream_id)
        if location is not None:
            params['location'] = location
        data = urllib.urlencode(params)
        js = self.util.get_json(self.util.get_live_stream_endpoint(), data)
        return self.util.json_to_objs(js, models.LiveStream)

    def get_locations(self):
        self.__check_logged_in()
        return self.util.json_to_objs(self.util.get_json(self.util.get_locations_endpoint(), ""), models.Location)

    def get_on_demand_dates(self):
        self.__check_premium()
        data = urllib.urlencode({
            'token': self.__get_token()
        })
        return self.util.get_json(self.util.get_on_demand_dates_endpoint(), data)['dates']

    def get_on_demand(self, date=None, team=None):
        self.__check_premium()
        params = {'token': self.__get_token()}
        if date is not None:
            params['date'] = date
        if team is not None:
            params['team'] = team
        data = urllib.urlencode(params)
        return self.util.json_to_objs(self.util.get_json(self.util.get_on_demand_endpoint(), data)['ondemand'], models.OnDemand)

    def get_on_demand_stream(self, on_demand_stream_id, location=None):
        self.__check_premium()
        params = {'token': self.__get_token(), 'id': on_demand_stream_id}
        if location is not None:
            params['location'] = location
        data = urllib.urlencode(params)
        return self.util.json_to_objs(self.util.get_json(self.util.get_on_demand_stream_endpoint(), data), models.OnDemandStream)

    def get_highlights(self,date=None, team_or_event=None):
        self.__check_premium()
        params = {'token': self.__get_token()}
        if date is not None:
            params['date'] = date
        if team_or_event is not None:
            params['team'] = team_or_event
        data = urllib.urlencode(params)
        return self.util.json_to_objs(self.util.get_json(self.util.get_highlights_endpoint(), data)['highlights'], models.Highlight)

    def get_condensed_games(self,date=None, team_or_event=None):
        self.__check_premium()
        params = {'token': self.__get_token()}
        if date is not None:
            params['date'] = date
        if team_or_event is not None:
            params['team'] = team_or_event
        data = urllib.urlencode(params)
        return self.util.json_to_objs(self.util.get_json(self.util.get_condensed_games_endpoint(), data)['condensed'], models.CondensedGame)

    def get_teams(self,league=None):
        self.__check_premium()
        params = {'token': self.__get_token()}
        if league is not None:
            params['league'] = league
        data = urllib.urlencode(params)
        return self.util.json_to_objs(self.util.get_json(self.util.get_list_teams_endpoint(), data)['teams'], models.Team)



