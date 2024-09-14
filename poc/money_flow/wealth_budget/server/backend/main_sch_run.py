from datetime import datetime
import pytz
import math

# Current Hour > offset just passed Midnight (-7)
# Select schedules with the offset (e.g. -7) and next_date = current_date
# s_past = [ s for schedules - check if s.time in the past ]
# execture transaction
# update schedule next time
# commit

def getTimezoneByOffset(offset_hour):
    tz_offsets = { -12: 'Etc/GMT+12',
                   -11: 'Pacific/Samoa', -10: 'Pacific/Honolulu', -9: 'US/Alaska',
                    -8: 'US/Pacific', -7: 'US/Arizona', -6: 'US/Central',
                    -5: 'America/New_York', -4: 'America/Santiago', -3: 'Canada/Newfoundland',
                    -2: 'America/Buenos_Aires', -1: 'America/Noronha', 0: 'GMT',
                     1: 'CET', 2: 'Europe/Istanbul', 3: 'Asia/Qatar',
                     4: 'Asia/Dubai', 5: 'Asia/Tashkent', 6: 'Asia/Bishkek',
                     7: 'Asia/Jakarta', 8: 'Asia/Singapore', 9: 'Asia/Seoul',
                    10: 'Australia/Sydney', 11: 'Pacific/Pohnpei', 12: 'Pacific/Fiji',
                    13: 'Pacific/Tongatapu', 14: 'Pacific/Kiritimati',  }
    return tz_offsets[offset_hour]

def whichOffsetIsJustAfterMidnight():
    curr_hour = datetime.now().astimezone(pytz.timezone('GMT')).hour
    tz_offset = 24 * math.floor(curr_hour/12) - curr_hour
    return tz_offset

def isDateInThePast(dt, offset):
    tz = getTimezoneByOffset(offset)
    local_time = pytz.timezone(tz).localize(datetime.fromisoformat(dt))
    curr_time = datetime.now().astimezone()
    date_is_in_the_past = False
    if curr_time > local_time:
        date_is_in_the_past = True
    print(date_is_in_the_past, 'for', tz)
    return date_is_in_the_past

print(getTimezoneByOffset(whichOffsetIsJustAfterMidnight()))

