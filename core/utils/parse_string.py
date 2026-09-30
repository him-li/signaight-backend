def parse_numeric_string(string: str):

    return int(eval(string.
                    replace('K', '*1000').
                    replace('M', '*1000000').
                    replace('B', '*1000000000')))
