import click
from click_configfile import (
    matches_section,
    Param,
    SectionSchema,
    ConfigFileReader
    )
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


class ConfigSectionSchema(object):
    """Describes all config sections of this configuration file."""

    @matches_section("Toggl")
    class TogglCF(SectionSchema):
        User = Param(type=str)
        Email = Param(type=str)
        Project = Param(type=str)
        Tags = Param(type=str)
        Description = Param(type=str)

    @matches_section("pyggl")   # Matches multiple sections
    class PygglCF(SectionSchema):
        period_per_day = Param(type=str)


class ConfigFileProcessor(ConfigFileReader):
    config_files = ["pyggl.ini", "pyggl.cfg", "pyggl.conf"]
    config_section_schemas = [
        ConfigSectionSchema.TogglCF,     # PRIMARY SCHEMA
        ConfigSectionSchema.PygglCF,
    ]


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


CONTEXT_SETTINGS = dict(
        help_option_names=['-h', '--help'],
        default_map=ConfigFileProcessor.read_config()
        )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-u", "--user", 'User', help="user name")
@click.option("-m", "--email", 'Email', required=True, help="user mail")
@click.option("-p", "--project", 'Project', help="project name")
@click.option("-t", "--tag", 'Tags', help="add tag")
@click.option("-d", "--description", 'Description', help="description")
@click.option("-f", "--config", type=click.Path(), default="pyggl.conf",
              help="configuration file")
@click.option("--out", type=click.Path(), default='taggle.csv',
              help="output name file")
@click.option("--period-per-day", 'period_per_day', default="9-12,14-18",
              help="Work interval per day")
@click.argument("period", type=click.DateTime(), nargs=-1,
                callback=my_period)
@click.pass_context
def main(ctx, **kargs):
    """Create CSV file for Toggl import.
    """
    try:
        kargs['start'], kargs['end'] = kargs.pop('period')
    except ValueError:
        click.secho("Missing date argument(s) !\n", fg="red", err=True)
        click.echo(ctx.get_help())
        return

    cmd = ToggleCmd(**kargs)
    cmd.write_csv()
    click.secho(f"Data added to `{kargs['out']}`", fg="green")


if __name__ == '__main__':
    main()
