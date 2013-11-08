__author__ = 'chuck'

import urllib2, json, sys

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

        def json_to_objs(self, js, model_type):
            if type(js) == list:
                retval = []
                for obj in js:
                    retval.append(self.json_to_objs(obj, model_type))
                return retval
            else:
                return model_type(js)

    __instance = None

    def __init__(self):
        if HSUtil.__instance is None:
            HSUtil.__instance = HSUtil.__impl()
        self.__dict__['_Singleton__instance'] = HSUtil.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)