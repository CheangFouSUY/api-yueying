from rest_framework import throttling


class anonRelaxed(throttling.AnonRateThrottle):
    scope='anon_relaxed'
    rate = '300/min'


class anonStricter(throttling.AnonRateThrottle):
    scope = 'anon_stricter'
    rate = '20/min'


class anonStrictest(throttling.AnonRateThrottle):
    scope = 'anon_strictest'
    rate = '5/min'


class userRelaxed(throttling.UserRateThrottle):
    scope = 'user_relaxed'
    rate = '500/min'


class userStrict(throttling.UserRateThrottle):
    scope = 'user_post_requests'
    rate = '60/day'


class userStricter(throttling.UserRateThrottle):
    scope = 'user_post_requests'
    rate = '20/day'


class userStrictest(throttling.UserRateThrottle):
    scope = 'user_post_requests'
    rate = '5/day'

