import click
import csv
from datetime import timedelta, time

""" Toggl for lazy people

Generate csv lines for toggl time tracking.
A simple tool to create one task for N days of continuous work on a time
period. For each day it split the task to allow a pause between mornig and
afternoon work.
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

    def get_rows(self, day):
        row_dict = {k: "" for k in self.header}
        # Morning
        mrow = {k: self.cmdargs[k] for k in row_dict.keys()
                if k in self.cmdargs}
        # TODO: hardcoded things
        mrow['Start date'] = day.date().isoformat()
        mrow['Start time'] = time(hour=9).isoformat()
        mrow['End date'] = day.date().isoformat()
        mrow['End time'] = time(hour=12).isoformat()
        mrow['Duration'] = '03:00:00'
        # Afternoon
        arow = {k: self.cmdargs[k] for k in row_dict.keys()
                if k in self.cmdargs}
        # TODO: hardcoded things
        arow['Start date'] = day.date().isoformat()
        arow['Start time'] = time(hour=14).isoformat()
        arow['End date'] = day.date().isoformat()
        arow['End time'] = time(hour=18).isoformat()
        arow['Duration'] = '04:00:00'
        return (mrow, arow)

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
                value = self.get_rows(day)
                writer.writerow(value[0])
                writer.writerow(value[1])


@click.command()
@click.option("-u", "--user", 'User', help="user name")
@click.option("-m", "--email", 'Email', required=True, help="user mail")
@click.option("-p", "--project", 'Project', default="", help="project name")
@click.option("-t", "--tag", 'Tag', default="", help="add tag")
@click.option("-d", "--description", 'Description',
              default="", help="description")
@click.option("--out", default='taggle.csv', help="output name file")
@click.argument("start", type=click.DateTime())
@click.argument("end", type=click.DateTime())
def taggle(**kargs):
    cmd = ToggleCmd(**kargs)
    cmd.write_csv()


if __name__ == '__main__':
    taggle()
