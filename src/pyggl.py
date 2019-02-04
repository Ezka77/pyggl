import click
import configparser
import csv
from datetime import timedelta, time
import datetime

"""Toggl for lazy people

... or in need of a time travel machine.

Generate csv lines for toggl time tracking system.
A simple tool to create one task for N days of continuous work on a time
period. For each day it split the task to allow a pause between morning and
afternoon work.

Not configurable things:
    - a day work is 9h00 to 12h00 and 14h00 to 18h00 (yeah =D)
    - a week is from Monday to Friday
"""


class ToggleCmd():
    header = [
            'User',
            'Email',
            'Project',
            'Description',
            'Start date',
            'Start time',
            'End date',
            'End time',
            'Duration',
            'Tags',
            ]

    def __init__(self, **kargs):
        self.cmdargs = kargs

    def get_time_row(self, day, hstart, hend):
        mrow = {k: self.cmdargs[k] for k in self.header
                if k in self.cmdargs}
        mrow['Start date'] = day.date().isoformat()
        mrow['Start time'] = time(hour=hstart).isoformat()
        mrow['End date'] = day.date().isoformat()
        mrow['End time'] = time(hour=hend).isoformat()
        mrow['Duration'] = str(timedelta(hours=hend) -
                               timedelta(hours=hstart))
        return mrow

    def write_rows(self, day, writer):
        # for eah interval get a row
        for i in self.get_period_per_day(self.cmdargs['period_per_day']):
            value = self.get_time_row(day, *list(i))
            writer.writerow(value)

    @staticmethod
    def weekday_gen(start, end):
        one_day = timedelta(days=1)
        day = start
        while day <= end:
            # if current day is a weekday return current day
            if day.weekday() < 5:
                yield day
            # add 1 day to current day
            day += one_day

    def write_csv(self):
        from os.path import exists
        filename = self.cmdargs['out']
        wgen = self.weekday_gen(self.cmdargs['start'], self.cmdargs['end'])
        is_header_needed = not exists(filename)

        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header)
            if is_header_needed:
                writer.writeheader()
            for day in wgen:
                self.write_rows(day, writer)

    @staticmethod
    def get_period_per_day(value):
        import re
        regex = r"([\d]{1,2})-([\d]{1,2})"
        matches = re.finditer(regex, value, re.MULTILINE)
        intervals = ((int(k) for k in match.groups()) for match in matches)
        return intervals


# For now use today at 0:0 time
today = datetime.datetime.combine(datetime.date.today(), datetime.time(0),)


def my_period(ctx, param, period):
    # One arg in period
    #  if today: start = end
    #  if < today: start = period[0] and end = today
    if len(period) == 1:
        if period[0] == today:
            return (period[0], period[0])
        if period[0] < today:
            return (period[0], today)
        if today < period[0]:
            return (today, period[0])
    return period[:2]


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-u", "--user", 'User', help="user name")
@click.option("-m", "--email", 'Email', help="user mail")
@click.option("-p", "--project", 'Project', help="project name")
@click.option("-t", "--tag", 'Tags', help="add tag")
@click.option("-d", "--description", 'Description', help="description")
@click.option("-f", "--config", type=click.Path(), default="pyggl.conf",
              help="configuration file")
@click.option("--out", type=click.Path(), default='taggle.csv',
              help="output name file")
@click.option("--period-per-day", 'period_per_day', default=None,
              help="Work interval per day")
@click.argument("period", type=click.DateTime(), nargs=-1,
                callback=my_period)
def main(**kargs):
    """Create CSV file for Toggl import.
    """
    kargs['start'], kargs['end'] = kargs.pop('period')
    # Try to read default Toggl configuration
    try:
        conf = configparser.ConfigParser()
        conf.optionxform = str
        conf.read(kargs['config'])
        d_conf = {k: v for k, v in conf.items('Toggl')}
    except configparser.NoSectionError:
        d_conf = {}
    # try to add pyggl defaults from configuration
    try:
        d_conf.update({k: v for k, v in conf.items('pyggl')})
    except configparser.NoSectionError:
        pass
    # remove None from kargs if set in d_conf
    d_args = {k: v for k, v in kargs.items()
              if k not in d_conf or v is not None}
    # update d_conf with d_args
    d_conf.update(d_args)
    try:
        assert(d_conf['Email'])
    except AssertionError:
        raise click.UsageError("missing parameter: 'Email'")
    if d_conf['period_per_day'] is None:
        d_conf['period_per_day'] = "9-12,14-18"
    # Start CMD
    cmd = ToggleCmd(**d_conf)
    cmd.write_csv()


if __name__ == '__main__':
    main()
