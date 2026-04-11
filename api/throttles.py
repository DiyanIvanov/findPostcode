from rest_framework.throttling import UserRateThrottle


class DailyThrottleRate(UserRateThrottle):
    scope = 'daily'

class PerMinuteThrottleRate(UserRateThrottle):
    scope = 'per-minute'
