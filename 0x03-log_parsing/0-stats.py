#!/usr/bin/python3
'''A script for parsing HTTP request logs.
'''
import re


def extract_input(log_entry):
    '''Extracts portion of a line of an HTTP request log.
    '''
    log_entry_pattern = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)'
    )
    extracted_info = {
        'status_code': 0,
        'file_size': 0,
    }
    log_format = '{}\\-{}{}{}{}\\s*'.format(
            log_entry_pattern[0],
            log_entry_pattern[1],
            log_entry_pattern[2],
            log_entry_pattern[3],
            log_entry_pattern[4])
    match_result = re.fullmatch(log_format, log_entry)
    if match_result is not None:
        http_status_code = match_result.group('status_code')
        size_of_file = int(match_result.group('file_size'))
        extracted_info['status_code'] = http_status_code
        extracted_info['file_size'] = size_of_file
    return extracted_info


def print_statistics(total_size_of_files, status_codes_count):
    '''Prints the accumulated statistics of the HTTP request log.
    '''
    print('Total file size: {:d}'.format(total_size_of_files), flush=True)
    for http_status_code in sorted(status_codes_count.keys()):
        count = status_codes_count.get(http_status_code, 0)
        if count > 0:
            print('{:s}: {:d}'.format(http_status_code, count), flush=True)


def update_metrics(log_line, total_size_of_files, status_codes_count):
    '''Updates the metrics from a given HTTP request log.

    Args:
        log_line (str): The line of input from which to retrieve the metrics.

    Returns:
        int: The new total file size.
    '''
    line_info = extract_input(log_line)
    http_status_code = line_info.get('status_code', '0')
    if http_status_code in status_codes_count.keys():
        status_codes_count[http_status_code] += 1
    return total_size_of_files + line_info['file_size']


def run():
    '''Starts the log parser.
    '''
    line_number = 0
    total_size_of_files = 0
    status_codes_count = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    try:
        while True:
            current_line = input()
            total_size_of_files = update_metrics(
                current_line,
                total_size_of_files,
                status_codes_count,
            )
            line_number += 1
            if line_number % 10 == 0:
                print_statistics(total_size_of_files, status_codes_count)
    except (KeyboardInterrupt, EOFError):
        print_statistics(total_size_of_files, status_codes_count)


if __name__ == '__main__':
    run()
