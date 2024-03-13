#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import webbrowser


def get_chats_file_name():
    return os.environ.get("CHATS_FILE") or sys.exit("CHATS_FILE environment variable isn't set")


def show_command(args):
    if not args.user and not args.channels:
        sys.exit("One of --user, --channels are required")
    forum_origin = os.environ.get("FORUM_ORIGIN") or "https://support.suretyhome.com"
    count = 0
    with open(get_chats_file_name(), newline='') as infile, open(args.output, 'w') as outfile:
        reader = csv.DictReader(infile)
        channels = args.channels.split(',') if args.channels else []
        for row in reader:
            if args.user and row['username'] == args.user and not row['chat_channel_id'] in channels:
                channels.append(row['chat_channel_id'])
            if row['chat_channel_id'] in channels:
                message = row['cooked'].replace('src="/uploads/', 'src="' + forum_origin + '/uploads/')
                outfile.write('<hr>' + row['username'] + " (" + row['created_at'] + "): " + message + '<br>')
                count += 1
    if count > 0:
        webbrowser.open('file://' + os.path.realpath(args.output))
    print("Showed " + str(count) + " messages in " + args.output)


def channels_command(args):
    if not args.user:
        sys.exit("--user is required")
    with open(get_chats_file_name(), newline='') as infile:
        reader = csv.DictReader(infile)
        channels = []
        for row in reader:
            if args.user and row['username'] == args.user and not row['chat_channel_id'] in channels:
                channels.append(row['chat_channel_id'])
    print(args.user + " was in channels " + ", ".join(channels))


parser = argparse.ArgumentParser(description='Discourse Chatbot chat history reader.')
subparsers = parser.add_subparsers(help='Available commands', required=True)

show_parser = subparsers.add_parser('show', help='Show chat history')
show_parser.add_argument('-u', '--user', help='The user whose chat history to show')
show_parser.add_argument('-c', '--channels', help='The chat channels to show')
show_parser.add_argument('-o', '--output', default='chat-history.html', help='File name to wite chat in')
show_parser.set_defaults(func=show_command)

channels_parser = subparsers.add_parser('channels', help='Show channels a user was in')
channels_parser.add_argument('-u', '--user', help='The user to show channels for')
channels_parser.set_defaults(func=channels_command)

args = parser.parse_args()
args.func(args)
