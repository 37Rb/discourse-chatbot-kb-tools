#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import json
from openai import OpenAI
from scipy.spatial.distance import cosine
from termcolor import colored


def by_header(row, header):
    headers = {
        'id': 0,
        'post': 1,
        'topic': 2,
        'post_number': 3,
        'topic_title': 4,
        'embedding': 5
    }
    return row[headers[header]]


def get_embedding(text):
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY environment variable isn't set")
    model = os.environ.get("EMBEDDINGS_MODEL") or "text-embedding-ada-002"
    client = OpenAI()
    return client.embeddings.create(input = [text], model=model).data[0].embedding


def embedding_command(args):
    print(get_embedding(args.query))


def get_embedding_file_name():
    return os.environ.get("EMBEDDINGS_FILE") or sys.exit("EMBEDDINGS_FILE environment variable isn't set")


def find_post_embedding_row(args):
    with open(get_embedding_file_name(), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            if args.embedding and args.embedding == int(by_header(row, 'id')):
                return row
            if args.post and args.post == int(by_header(row, 'post')):
                return row
            if args.topic and args.topic == int(by_header(row, 'topic')) and args.number == int(by_header(row, 'post_number')):
                return row
    return None


def similarity_command(args):
    if not args.embedding and not args.post and not args.topic and not args.file and not args.string:
        sys.exit("One of --embedding, --post, --topic, --file, or --string are required")
    query_embedding = get_embedding(args.query)
    if args.string:
        embedding = get_embedding(args.string)
        print("Similarity to the given string is " + format(1 - cosine(query_embedding, embedding), '.6f'))
    elif args.file:
        with open(args.file, 'r') as f:
            embedding = get_embedding(f.read())
            print("Similarity to the contents of " + args.file + " is " + format(1 - cosine(query_embedding, embedding), '.6f'))
    else:
        row = find_post_embedding_row(args) or sys.exit("Could not find post embedding")
        embedding = json.loads(by_header(row, 'embedding'))
        print("Similarity to topic " + by_header(row, 'topic') + " post " + by_header(row, 'post_number') + " is " + format(1 - cosine(query_embedding, embedding), '.6f'))


def search(query, limit):
    query_embedding = get_embedding(query)

    results = []
    with open(get_embedding_file_name(), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            post_embedding = json.loads(by_header(row, 'embedding'))
            similarity = 1 - cosine(query_embedding, post_embedding)
            results.append({
                'topic': by_header(row, 'topic').strip(),
                'number': by_header(row, 'post_number').strip(),
                'similarity': similarity,
                'title': by_header(row, 'topic_title')
            })

    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:limit]


def search_command(args):
    results = search(args.query, args.limit)
    for i, result in enumerate(results):
        print(str(i+1) + ") topic " + str(result['topic']) + " post " + str(result['number']) + " similarity " + format(result['similarity'], '.6f') + ": " + result['title'])


def run_test(topic, post_number, in_top, query):
    results = search(query, in_top)
    for result in results:
        if post_number:
            if result['topic'] == topic and result['number'] == post_number:
                return None
        else:
            if result['topic'] == topic:
                return None
    return results


def test_command(args):
    with open(args.file, newline='') as tests_file:
        reader = csv.DictReader(tests_file)
        passed = 0
        failed = 0
        for test in reader:
            topx = run_test(test['Topic'].strip(), test['Post Number'].strip(), int(test['In Top']), test['Query'])
            if topx:
                failed += 1
                post_part = " post " + test['Post Number'] if test['Post Number'].strip() else ""
                print(colored("Failed!", 'red') + " topic " + test['Topic'] + post_part + " not in top " + test['In Top'] + ' for "' + test['Query'] + '"')
                if args.verbose:
                    for i, result in enumerate(topx):
                        print("    " + str(i+1) + ") topic " + str(result['topic']) + " post " + str(result['number']) + " similarity " + format(result['similarity'], '.6f') + ": " + result['title'])
            else:
                passed += 1

        print("Ran " + str(passed + failed) + " tests: " + colored(str(passed) + " passed", 'green') + ", " + colored(str(failed) + " failed", 'red'))


parser = argparse.ArgumentParser(description='Discourse Chatbot embedding tools.')
subparsers = parser.add_subparsers(help='Available commands', required=True)

show_parser = subparsers.add_parser('embedding', help='Show the embedding for a query')
show_parser.add_argument('query', help='The query')
show_parser.set_defaults(func=embedding_command)

similarity_parser = subparsers.add_parser('similarity', help='Show the similarity between a post, file, or string and a query')
similarity_parser.add_argument('-e', '--embedding', type=int, help='Compare to the embedding with ID')
similarity_parser.add_argument('-p', '--post', type=int, help='Compare to the post with ID')
similarity_parser.add_argument('-t', '--topic', type=int, help='Compare to a post in the topic with ID')
similarity_parser.add_argument('-n', '--number', type=int, default=1, help='The post number in a topic (used with --topic)')
similarity_parser.add_argument('-f', '--file', help='Compare to the contents of a file')
similarity_parser.add_argument('-s', '--string', help='Compare the query to a given string')
similarity_parser.add_argument('query', help='The query')
similarity_parser.set_defaults(func=similarity_command)

search_parser = subparsers.add_parser('search', help='Show search results for a query')
search_parser.add_argument('-l', '--limit', type=int, default=10, help='Show this many search results')
search_parser.add_argument('query', help='The query')
search_parser.set_defaults(func=search_command)

test_parser = subparsers.add_parser('test', help='Test search results against expectations')
test_parser.add_argument('-v', '--verbose', action='store_true', help='Show additional information about failures')
test_parser.add_argument('file', help='The file containing search result expectations')
test_parser.set_defaults(func=test_command)

args = parser.parse_args()
args.func(args)
