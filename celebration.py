#!/usr/bin/env python3
from functools import reduce
import re

# Chain of days
# Most people per day
# Longest streak
# Most celebrations

from collections import defaultdict
from datetime import datetime
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super(SetEncoder, self).default(obj)

def main():
    opened = open("./irc.esper.#merveilles.weechatlog")
    compiled = re.compile(r"\tA*$")

    dates_celebrated_by_who = defaultdict(set)
    screaming_moments_by_who = defaultdict(set)
    who_chain = defaultdict(lambda: 0)
    screaming_chain = defaultdict(lambda: 0)

    found_first = False
    screaming_found_first = False
    most_recent_date = None
    for line in opened:
        date_str = line[:19]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        if "happy void day" in line.lower() and "topic for #merveilles" not in line:
            split = line.split("\t")
            username = split[1].replace("@", "")
            key = '{}-{}-{}'.format(date_obj.year, date_obj.month, date_obj.day)
            dates_celebrated_by_who[key].add(username)
            who_chain[username] += 1

            if found_first is False:
                found_first = {"when": key, "who": username}
        elif re.search(r"\tA+$", line) is not None:
            split = line.split("\t")
            username = split[1].replace("@", "")
            key = '{}-{}-{}'.format(date_obj.year, date_obj.month, date_obj.day)
            screaming_moments_by_who[key].add(username)
            screaming_chain[username] += 1

            if screaming_found_first is False:
                screaming_found_first = {"when": key, "who": username}
        most_recent_date = date_obj
    opened.close()

    delta = most_recent_date - datetime.strptime(found_first["when"], "%Y-%m-%d")
    times_celebrated = len(dates_celebrated_by_who.keys())
    final = {"times_celebrated": times_celebrated,
            "dates_celebrated": dates_celebrated_by_who,
            "days_since_first_celebration": delta.days,
            "celebration_score": "{}/{}".format(times_celebrated, delta.days),
            "celebrated_count": who_chain,
            "screaming_count": screaming_chain,
            "first_celebrated": found_first,
            "first_scream_celebrated": screaming_found_first,
            "who_had_most_celebrations": reduce(lambda accum, val: accum if accum[1] > val[1] else val, who_chain.items(), ("x", -1)),
            "when_had_most_celebrations": reduce(lambda accum, val: accum if len(accum[1]) > len(val[1]) else val, dates_celebrated_by_who.items(), ("x", [])),
            "who_had_most_screams": reduce(lambda accum, val: accum if accum[1] > val[1] else val, screaming_chain.items(), ("x", -1)),
            "when_had_most_screams": reduce(lambda accum, val: accum if len(accum[1]) > len(val[1]) else val, screaming_moments_by_who.items(), ("x", [])),
            "longest_streak": "???"
            }
    print(json.dumps(final, cls=SetEncoder))


if __name__ == '__main__':
    main()
