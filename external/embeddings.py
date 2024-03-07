#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import json
from openai import OpenAI
from scipy.spatial.distance import cosine


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
    client = OpenAI()
    return client.embeddings.create(input = [text], model="text-embedding-ada-002").data[0].embedding


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
    if not args.embedding and not args.post and not args.topic:
        sys.exit("One of --embedding, --post, or --topic are required to find the post embedding")
    query_embedding = get_embedding(args.query)
    row = find_post_embedding_row(args) or sys.exit("Could not find post embedding")
    post_embedding = json.loads(by_header(row, 'embedding'))
    print("Similarity to topic " + by_header(row, 'topic') + " post " + by_header(row, 'post_number') + " is " + format(1 - cosine(query_embedding, post_embedding), '.6f'))


def search_command(args):
    query_embedding = get_embedding(args.query)

    results = []
    with open(get_embedding_file_name(), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            post_embedding = json.loads(by_header(row, 'embedding'))
            similarity = 1 - cosine(query_embedding, post_embedding)
            results.append({
                'topic': by_header(row, 'topic'),
                'number': by_header(row, 'post_number'),
                'similarity': similarity,
                'title': by_header(row, 'topic_title')
            })

    results.sort(key=lambda x: x['similarity'], reverse=True)
    count = 0
    for result in results[:args.limit]:
        count += 1
        print(str(count) + ") topic " + str(result['topic']) + " post " + str(result['number']) + " similarity " + format(result['similarity'], '.6f') + ": " + result['title'])


parser = argparse.ArgumentParser(description='Discourse Chatbot embedding tools.')
subparsers = parser.add_subparsers(help='Available commands', required=True)

show_parser = subparsers.add_parser('embedding', help='Show the embedding for a query')
show_parser.add_argument('query', help='The query')
show_parser.set_defaults(func=embedding_command)

similarity_parser = subparsers.add_parser('similarity', help='Show the similarity between a post embedding and a query')
similarity_parser.add_argument('-e', '--embedding', type=int, help='The embedding ID')
similarity_parser.add_argument('-p', '--post', type=int, help='The post ID')
similarity_parser.add_argument('-t', '--topic', type=int, help='The topic ID')
similarity_parser.add_argument('-n', '--number', type=int, default=1, help='The post number in a topic')
similarity_parser.add_argument('query', help='The query')
similarity_parser.set_defaults(func=similarity_command)

search_parser = subparsers.add_parser('search', help='Show search results for a query')
search_parser.add_argument('-l', '--limit', type=int, default=10, help='Show this many search results')
search_parser.add_argument('query', help='The query')
search_parser.set_defaults(func=search_command)

args = parser.parse_args()
args.func(args)
