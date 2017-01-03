#!/usr/bin/env python2

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

    dates_celebrated_by_who = defaultdict(set)
    who_chain = defaultdict(lambda: 0)

    max_days_celebrated = 0

    found_first = False
    for line in opened:
        date_str = line[:19]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        if "happy void day" in line.lower() and "topic for #merveilles" not in line:
            split = line.split("\t")
            username = split[1].replace("@", "")
            key = '{}-{}-{}'.format(date_obj.year, date_obj.month, date_obj.day)
            dates_celebrated_by_who[key].add(username)
            who_chain[username] += 1

            if len(dates_celebrated_by_who[key]) == 1:
                max_days_celebrated += 1

            if found_first is False:
                found_first = {"when": key, "who": username}
    opened.close()

    final = {"times_celebrated": max_days_celebrated,
            "dates_celebrated": dates_celebrated_by_who,
            "celebrated_count": who_chain,
            "first_celebrated": found_first,
            }
    print json.dumps(final, cls=SetEncoder)


if __name__ == '__main__':
    main()
