import json
import time
import datetime
from dateutil import tz
from dateutil.parser import parse
from devices.external_api import ExternalApi

to_zone = tz.gettz('America/Mexico_City')
class SolcastApi(ExternalApi):

    def __init__(self, name, init, messager):
        ExternalApi.__init__(self, name, init, messager)



    def parse(self, message):
        parsed_m = []
        try:
            message_p = json.loads(message['data'])
            self.internal_state = message_p
            time_now = datetime.datetime.now().replace(tzinfo = to_zone)
            self.state = self.get_radiation(time_now)

        except Exception as ex:
            print("Error parsing api message "+ self.name) 
            print(ex)
            raise
        return parsed_m

    def get_radiation(self, time_now):
        rad_data = self.internal_state
        forecasts = rad_data['forecasts']
        ghi_series = []
        period_end = []
        for ff in forecasts:
            radiation = ff['ghi']
            p_end = parse(ff['period_end']).astimezone(to_zone)
            if(p_end > time_now and p_end < time_now + datetime.timedelta(hours = 12)):
                ghi_series.append(radiation)
                period_end.append(p_end)
        print(ghi_series)
        len_rad = len(ghi_series)
        periods = 6
        last_chance = len_rad - periods
        best_index = 0
        best_sum = 0
        for i in range(0, last_chance):
            acum = sum(ghi_series[i:(i+periods)])
            if(acum > best_sum):
                best_index = i
                best_sum = acum
        best_time = period_end[best_index]
        return {'best_index':best_index, 'best_sum':best_sum, 'best_time':str(best_time)}
