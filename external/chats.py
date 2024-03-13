#!/usr/bin/env python3

import sys
import os
import argparse
import csv
from datetime import datetime, date
import webbrowser


def for_each_csv_row(args, callback):
    csv_file_name = os.environ.get("CHATS_FILE") or sys.exit("CHATS_FILE environment variable isn't set")
    from_date = datetime.strptime(args.from_date, '%Y-%m-%d').date() if args.from_date else None
    to_date = datetime.strptime(args.to_date, '%Y-%m-%d').date() if args.to_date else None
    with open(csv_file_name, newline='') as infile:
        reader = csv.DictReader(infile)
        channels = args.channels.split(',') if hasattr(args, 'channels') and args.channels else []
        for row in reader:
            created_on = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S %Z')
            if from_date and created_on.date() < from_date:
                continue
            if to_date and created_on.date() > to_date:
                continue
            if args.user and row['username'] == args.user and not row['chat_channel_id'] in channels:
                channels.append(row['chat_channel_id'])
            callback(channels, row)


def show_command(args):
    if not args.user and not args.channels:
        sys.exit("One of --user, --channels are required")
    forum_origin = os.environ.get("FORUM_ORIGIN") or "https://support.suretyhome.com"
    count = 0
    with open(args.output, 'w') as outfile:
        def write_message_if_in_channel(channels, row):
            nonlocal count
            if row['chat_channel_id'] in channels:
                message = row['cooked'].replace('src="/uploads/', 'src="' + forum_origin + '/uploads/')
                outfile.write('<hr>' + row['username'] + " (" + row['created_at'] + "): " + message + '<br>')
                count += 1
        for_each_csv_row(args, write_message_if_in_channel)
    if count > 0:
        webbrowser.open('file://' + os.path.realpath(args.output))
    print("Showed " + str(count) + " messages in " + args.output)


def channels_command(args):
    if not args.user:
        sys.exit("--user is required")
    channels = []
    def update_channels(new_channels, row):
        nonlocal channels
        channels = new_channels
    for_each_csv_row(args, update_channels)
    print(args.user + " was in channels " + ", ".join(channels))


parser = argparse.ArgumentParser(description='Discourse Chatbot chat history reader.')
subparsers = parser.add_subparsers(help='Available commands', required=True)

show_parser = subparsers.add_parser('show', help='Show chat history')
show_parser.add_argument('-u', '--user', help='The user whose chat history to show')
show_parser.add_argument('-c', '--channels', help='The chat channels to show')
show_parser.add_argument('-f', '--from-date', help='Only include messages from this date')
show_parser.add_argument('-t', '--to-date', help='Only include messages up to this date')
show_parser.add_argument('-o', '--output', default='chat-history.html', help='File name to wite chat in')
show_parser.set_defaults(func=show_command)

channels_parser = subparsers.add_parser('channels', help='Show channels a user was in')
channels_parser.add_argument('-u', '--user', help='The user to show channels for')
channels_parser.add_argument('-f', '--from-date', help='Only include messages from this date')
channels_parser.add_argument('-t', '--to-date', help='Only include messages up to this date')
channels_parser.set_defaults(func=channels_command)

args = parser.parse_args()
args.func(args)
