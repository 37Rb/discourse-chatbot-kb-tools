# Discourse Chatbot Knowledge Base Tools
Knowledge base management tools for Discourse Chatbot

Discourse Chatbot is an AI chatbot plugin for Discourse that can be used to make a support bot on your forum. Visit [Meta](https://meta.discourse.org/t/discourse-chatbot-now-smarter-than-chatgpt/256652) and [Github](https://github.com/merefield/discourse-chatbot) to learn more about it.

Discourse Chatbot uses [RAG](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts) to provide the AI model with domain-specific knowledge of your forum. While it's possible to let the bot access every public post on your forum, it may be benficial to limit access to a specific, non-public "knowledge base" category where you curate only high-quality posts that you want the bot to see.

Discourse Chatbot semantic-searches the forum for individual posts instead of topics which makes it challenging for the bot to find complete questions and answers. Often the question/problem is in one post while the answer/solution is in a later post. There may even be multiple back and forth posts leading up the the answer. The topic title and tags may also be useful to the bot but aren't included in this search because it's limited to posts.

Chatbot Knowledge Base Tools help you import knowledge from your forum & website into the knowledge base category in a format that's well-suited for the bot. For example, you can:

* Import entire topics into the knowledge base as a single post so that the bot can see the entire conversation with all relevent context.
* Import pages from your website into the knowledge base so the bot can use them in addition to your forum content.

## Usage

A JavaScript object called ChatbotKnowledgeBase provides access to the tools. Use the [JavaScript console](https://www.coursera.support/s/article/learner-000001653-How-to-open-the-Javascript-console?language=en_US) in your browser while at your Discourse forum to create an instance of ChatbotKnowledgeBase and call its functions. You need to be logged in.

![Example Javascript Console](https://raw.githubusercontent.com/37Rb/discourse-chatbot-kb-tools/main/images/example-js-console.png)

### Create the ChatbotKnowledgeBase object

Create a new ChatbotKnowledgeBase object and assign it to a variable.

```javascript
x = new ChatbotKnowledgeBase()
```

By default, it will look for a category named Chatbot to use as the knowledge base category. If your knowledge base categiory has a different name, you can provide it when you create the object.

```javascript
x = new ChatbotKnowledgeBase("My Knowledge Base Category")
```

### Import a Topic

Use importTopic() to import a topic into the knowledge base.

```javascript
importTopic(topicId, options)
```

* topicId - The source topic ID
* options - An object to specify optional behavior. Available options are
  * update: KB topic ID - Update an existing KB topic instead of creating a new one
  * include: Array of post numbers - Only include the given post numbers
  * exclude: Array of post numbers - Exclude the given post numbers

#### Examples

Import topic 26970 as a new KB topic.

```javascript
x.importTopic(26970)
```

Import topic 26989 by updating KB topic 27102. Do this when a topic that's already been imported has changed.

```javascript
x.importTopic(26989, { update: 27102 })
```

Only include posts 1, 2, and 4 in the KB topic.

```javascript
x.importTopic(26989, { include: [1,2,4] })
```

Exclude posts 3, 5, and 6 from the KB topic.

```javascript
x.importTopic(26989, { exclude: [3,5,6] })
```

### Import a Category

Use importCategory() to import (or update) every topic in a category.

```javascript
importCategory(categoryName, options)
```

* categoryName: The name of the category to import from
* options - An object to specify optional behavior. Available options are
  * limit: Integer - Only import the *limit* latest topics in the category

Use await with importCategory() so that you can see when it's done.

#### Examples

Import (or update) every topic in the How To category.

```javascript
await x.importCategory("How To")
```

Import (or update) the 25 latest topics in the How To category.

```javascript
await x.importCategory("How To", { limit: 25 })
```

### Import a Web Page

Use importWebPage() to import a web page into the knowledge base.

```javascript
importWebPage(url, options)
```

* url - The URL if the web page
* options - An object to specify optional behavior. Available options are
  * update: KB topic ID - Update an existing KB topic instead of creating a new one
  * removeTags: Array of HTML tags - Don't import content in these tags
  * removeIds: Array of HTML IDs - Don't import content in in elements with these IDs
  * dryRun: Boolean - Just print the markdown without importing anything

importWebPage() uses [Turndown](https://github.com/mixmark-io/turndown) to convert HTML pages to markdown before importing them into the knowledge base.

Web pages have a lot of extra stuff you probably don't want to import. Use the removeTags and removeIds options to exclude content you don't want in the knowledge base.

Tags in the defaultImportWebPageRemoveTags property are exluded by default. You can modify this or create a new array for the removeTags option.

```javascript
x.defaultImportWebPageRemoveTags = ['meta', 'style', 'link', 'script', 'noscript', 'applet', 'area', 'object', 'nav', 'base', 'embed', 'object', 'param', 'header', 'hgroup', 'footer']
```

#### Examples

Import https://suretyhome.com/why-surety/ as a new KB topic.

```javascript
x.importWebPage("https://suretyhome.com/why-surety/")
```

Import https://suretyhome.com/why-surety/ by updating KB topic 28500. Do this when a web page that's already been imported has changed.

```javascript
x.importWebPage("https://suretyhome.com/why-surety/", { update: 28500 })
```

Don't include any content in the div with ID = "mini-cart".

```javascript
x.importWebPage("https://suretyhome.com/why-surety/", { removeIds: ["mini-cart"] })
```

Show the markdown instead of importing it into the knowledge base.

```javascript
x.importWebPage("https://suretyhome.com/why-surety/", { dryRun: true })
```

### Update All Imports

Use updateAllImports() to update all existing imports that have changed.

```javascript
updateAllImports(types = ['topic', 'page'])
```

* types: Array of import types - The types to update, defaults to all

Use await with updateAllImports() so that you can see when it's done.

#### Examples

Update all imports. (of all types)

```javascript
await x.updateAllImports()
```

Update all topic imports.

```javascript
await x.updateAllImports(['topic'])
```

## Installation

### Install Theme Component

Install as a theme component from the Git repository.

https://github.com/37Rb/discourse-chatbot-kb-tools.git

### Security Setup

ImportWebPage needs to access resources on other domains. You need to configure [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) and [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) to allow it.

Configure [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) by in Discourse admin *content security policy script src* setting (found under Security). Add https://unpkg.com/turndown/dist/turndown.js as a script source so that [Turndown](https://github.com/mixmark-io/turndown) can be loaded.

Configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) by adding an [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) HTTP header to the website you will import from allowing your Discourse forum origin (https:// and domain name) to access content on that website. Alternatively, you can disable CORS checks in your browser when importing web pages.

### JavaScript Console

#### Why JavaScript Console?

KB tools are used via the JavaScript console because it's the easiest way to run code as a logged in user without having to pass around API keys or develop a GUI. If they get heavily used it may make sense in the future to build them into the Discourse GUI.

#### Hide Network Errors

Sometimes the Discourse API responds with an error status code even during normal usage. For example

* If you try to import a topic that's already been imported without using the update option then the API will respond with 422 Unprocessable Content.
* During bulk imports the API will sometimes respond with 429 Too Many Requests, asking the client to slow down.

These are normal and the tools handle them fine but the Javascript console might show them as big red errors which is annoying. You can [configure it to hide those](https://developer.chrome.com/docs/devtools/console/reference#network).

# Discourse Chatbot Embedding Tools

Semantic search is great but trying to optimize or troubleshoot it can be difficult because it happens behind the scenes. Embeddings Tools is a command line program that helps you see what's happening behind the curtain. You can easily

* Run a semantic search and see which posts show up at the top, along with their similary scores
* Calulate the similarity score between a search query and post embedding
* Get an embedding for a search query from OpenAI

## Usage

It's a python script that lives in the "external" folder of the Git repository.

```
% cd external
% ./embeddings.py -h
usage: embeddings.py [-h] {embedding,similarity,search} ...

Discourse Chatbot embedding tools.

positional arguments:
  {embedding,similarity,search}
                        Available commands
    embedding           Show the embedding for a query
    similarity          Show the similarity between a post embedding and a query
    search              Show search results for a query

options:
  -h, --help            show this help message and exit
```

### Run Semantic Search

Show the top search results of a semantic search for the query across all the post embeddings.

```
% ./embeddings.py search -h
usage: embeddings.py search [-h] [-l LIMIT] query

positional arguments:
  query                 The query

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Show this many search results
```

#### Examples

Semantic search for the query, "Mount a PG9303".

```
% ./embeddings.py search "Mount a PG9303"
```

Semantic search for the query, "Mount a PG9303" and only show the top 3 results.

```
% ./embeddings.py search "Mount a PG9303"  --limit 3
```

### Calculate Similarity Score

Calculate the similarity score between a query and a specific post embedding. The similarity score is 1 minus the cosine distance between the query embedding and the post embedding.

```
% ./embeddings.py similarity -h                    
usage: embeddings.py similarity [-h] [-e EMBEDDING] [-p POST] [-t TOPIC] [-n NUMBER] query

positional arguments:
  query                 The query

options:
  -h, --help            show this help message and exit
  -e EMBEDDING, --embedding EMBEDDING
                        The embedding ID
  -p POST, --post POST  The post ID
  -t TOPIC, --topic TOPIC
                        The topic ID
  -n NUMBER, --number NUMBER
                        The post number in a topic
```

One of --embedding, --post, or --topic are required to find the post embedding that the query will be compared to.

#### Examples

Show the similarity score between the first post in topic 28476 and the query, "Mount a PG9303".

```
 % ./embeddings.py similarity "Mount a PG9303" --topic 28476
```

### Get Embedding

Get the embedding vector for a query from OpenAI.

```
% ./embeddings.py embedding -h
usage: embeddings.py embedding [-h] query

positional arguments:
  query       The query

options:
  -h, --help  show this help message and exit
```

#### Examples

```
% ./embeddings.py embedding "Mount a PG9303"
```

## Installation

Clone the Git repository.

```
% git clone https://github.com/37Rb/discourse-chatbot-kb-tools.git
```

The script requires Python3 to be installed. Then install these pip packages.

```
% pip install scipy
% pip install openai
```

Export your Chatbot embeddings to a CSV file using the [Data Explorer](https://www.discourse.org/plugins/data-explorer.html) plugin. Create the following query.

```sql
SELECT e.id, e.post_id AS post, p.topic_id AS topic, p.post_number,
       t.title as topic_title, e.embedding
FROM chatbot_post_embeddings e LEFT JOIN
     posts p ON e.post_id = p.id JOIN
     topics t ON p.topic_id = t.id
WHERE p.deleted_at IS NULL
```

Run it and then download the results as CSV. Once downloaded, set your EMBEDDINGS_FILE environment variable as the path to that CSV file. This is how the script can search your embeddings.

```
% export EMBEDDINGS_FILE=~/Downloads/chatbot-embeddings-blah-blah-blah.csv
```

Set your OPENAI_API_KEY environment variable to an API key you get from your OpenAI account.

```
% export OPENAI_API_KEY=XXXXXXXXXXXXXXXXXXXXXXX
```

Now you should be able to run the script.