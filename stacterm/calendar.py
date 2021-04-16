import calendar


def print_labeled_calendar(events, label_field, cols=3):
    """ Get calendar covering all dates, with provided dates colored and labeled """
    if len(events.keys()) == 0:
        return ''
    # events is {'date': 'label'}
    _dates = sorted(events.keys())
    _labels = set(events.values())
    labels = dict(zip(_labels, [str(41 + i) for i in range(0, len(_labels))]))

    start_year = _dates[0].year
    end_year = _dates[-1].year

    # start and end rows
    row1 = int((_dates[0].month - 1) / cols)
    row2 = int((_dates[-1].month - 1) / cols) + 1

    # generate base calendar array
    Calendar = calendar.Calendar()
    cal = []
    for yr in range(start_year, end_year + 1):
        ycal = Calendar.yeardatescalendar(yr, width=cols)
        if yr == start_year and yr == end_year:
            ycal = ycal[row1:row2]
        elif yr == start_year:
            ycal = ycal[row1:]
        elif yr == end_year:
            ycal = ycal[:row2]
        cal.append(ycal)

    # month and day headers
    months = calendar.month_name
    days = 'Mo Tu We Th Fr Sa Su'
    hformat = '{:^20}  {:^20}  {:^20}\n'
    rformat = ' '.join(['{:>2}'] * 7) + '  '

    # create output
    col0 = '\033['
    col_end = '\033[0m'
    out = ''
    for iy, yrcal in enumerate(cal):
        out += '{:^64}\n\n'.format(_dates[0].year + iy)
        for mrow in yrcal:
            mnum = mrow[0][2][3].month
            names = [months[mnum], months[mnum + 1], months[mnum + 2]]
            out += hformat.format(names[0], names[1], names[2])
            out += hformat.format(days, days, days)
            for r in range(0, len(mrow[0])):
                for c in range(0, cols):
                    if len(mrow[c]) == 4:
                        mrow[c].append([''] * 7)
                    if len(mrow[c]) == 5:
                        mrow[c].append([''] * 7)
                    wk = []
                    for d in mrow[c][r]:
                        if d == '' or d.month != (mnum + c):
                            wk.append('')
                        else:
                            string = str(d.day).rjust(2, ' ')
                            if d in _dates:
                                string = '%s%sm%s%s' % (
                                    col0, labels[events[d]], string, col_end)
                            wk.append(string)
                    out += rformat.format(*wk)
                out += '\n'
            out += '\n'
    # print labels
    out += f"{label_field}:\n"
    for lbl, col in labels.items():
        # vals = list(_labels)
        out += '  %s%sm%s %s\n' % (col0, col, lbl, col_end)
    print(out)
