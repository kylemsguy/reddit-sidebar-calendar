#!/usr/bin/env python3

from calendar import TextCalendar
from datetime import date

days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

def deep_copy(inList: list) -> list:
    """Makes a deep copy of a list of lists"""
    if isinstance(inList, list):
        return list( map(deep_copy, inList) )
    return inList


def is_leap_year(year: int) -> bool:
    """Returns whether the given year is a leap year"""
    if year % 100 == 0:
        return year % 400 == 0
    else:
        return year % 4 == 0

def get_month_ary(year: int, month: int) -> list:
    """Get the formatted month as a list of lists"""
    c = TextCalendar()

    month_str = c.formatmonth(year, month)
    weeks = month_str.split('\n')

    title = weeks[0].strip()
    weeks = weeks[1:]

    month = [title]
   
    for week in weeks:
        week_list_stripped = week.strip()
        week_list_split_filtered = list(filter(None, week_list_stripped.split(' ')))
        month.append(week_list_split_filtered)

    if not month[-1]:
        month.pop()

    return month[:]

def add_preceding_days(year: int, month: int, month_ary: list) -> list:
    """Adds preceding days to the first week of the month in-place"""
    # check if February
    if month == 1:
        # check if leap year
        prev_days = days_in_month[month] + int(is_leap_year())
    else:
        prev_days = days_in_month[month]

    first_week = month_ary[2]
    i = 0
    while len(first_week) < 7:
        first_week.insert(0, str(prev_days - i))
        i += 1
    return month_ary

def add_trailing_days(month_ary: list) -> list:
    """Adds trailing days to the last week of the month in-place."""
    last_week = month_ary[-1]
    day = 1
    while len(last_week) < 7:
        last_week.append(str(day))
        day += 1

    return month_ary

def format_markdown(shortdaywk: bool, month_ary: list) -> str:
    """Formats the given month array as markdown, adding any padding necessary"""
    # make a copy so that we don't destroy the original
    month = deep_copy(month_ary)

    title = month[0]
    header = month[1]
    month = month[2:]

    # pad the first and last week accordingly
    first_week = month[0]
    while len(first_week) < 7:
        first_week.insert(0, ' ')

    last_week = month[-1]
    while len(last_week) < 7:
        last_week.append(' ')

    # convert to Markdown
    ## add title
    md_month = ['__', title, '__', '\n']

    ## add day of the week as header
    md_month.append('| ')
    
    for day in header:
        if shortdaywk:
            md_month.append(day[0])
        else:
            md_month.append(day)

        md_month.append(' |')
        md_month.append(' ')

    md_month[-1] = '\n'
    md_month.append('|')

    ## add header divider
    for i in range(7):
        md_month.append(" --- |")

    md_month.append('\n')

    ## add rest of the days
    for week in month:
        if(len(week) != 7):
            raise IndexError("Week length not 7")

        md_month.append('| ')

        for day in week:
            md_month.append(day)
            md_month.append(" |")
            md_month.append(' ')

        md_month[-1] = '\n'

    return ''.join(md_month)

if __name__ == "__main__":
    today_year = date.today().year
    today_month = date.today().month

    year = input("What year? [" + str(today_year) + "]: ")
    month = input("What month? [" + str(today_month) + "]: ")

    if not year:
        year = today_year
    else:
        year = int(year)
    if not month:
        month = today_month
    else:
        month = int(month)

    trailing = input("Add preceding and trailing days? [Y/n]: ")
    shortdaywk = input("Single-character days of the week? [Y/n]: ")

    if not trailing:
        trailing = True
    elif trailing == 'y' or trailing == 'Y':
        trailing = True
    else:
        trailing = False

    if not shortdaywk:
        shortdaywk = True
    elif shortdaywk == 'y' or shortdaywk == 'Y':
        shortdaywk = True
    else:
        shortdaywk = False

    raw_month = get_month_ary(year, month)

    if trailing:
        add_preceding_days(year, month, raw_month)
        add_trailing_days(raw_month)

    formatted_month = format_markdown(shortdaywk, raw_month)

    print()
    write_to_file = input("Specify filename or leave blank to print to console: ")
    print()
    print()
    if not write_to_file:
        print(formatted_month)
    else:
        with open(write_to_file, 'w') as out_file:
            out_file.write(formatted_month)
