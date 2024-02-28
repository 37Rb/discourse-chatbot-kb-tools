# Discourse Chatbot Knowledge Base Tools
Knowledge base management tools for Discourse Chatbot

Discourse Chatbot is an AI chatbot plugin for Discourse that can be used to make a support bot on your forum. Visit [Meta](https://meta.discourse.org/t/discourse-chatbot-now-smarter-than-chatgpt/256652) and [Github](https://github.com/merefield/discourse-chatbot) to learn more about it.

Discourse Chatbot uses [RAG](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts) to provide the AI model with domain-specific knowledge on your forum. While it's possible to let the bot access every public post on your forum, it may be benficial to limit access to a specific, non-public knowledge base category where you curate only high-quality posts that you want the bot to see when helping users. 

Discourse Chatbot semantic-searches the forum for individual posts instead of topics which makes it challenging for the bot to find complete questions and answers. Often the question/problem is in one post while the answer/solution is in a later post. There may even be multiple back and forth posts leading up the the answer. The topic title and tags may also be useful to the bot but aren't in posts.

Chatbot Knowledge Base Tools help you import knowledge from your forum into the knowledge base category in a form that's easier for the bot to find and use. For example, you can import entire topics into the knowledge base as a single post so that the bot can see the entire conversation with all relevent context.

## Usage

A JavaScript object called ChatbotKnowledgeBase provides access to the tools. Use the [JavaScript console](https://www.coursera.support/s/article/learner-000001653-How-to-open-the-Javascript-console?language=en_US) in your browser to create an instance of ChatbotKnowledgeBase and call its functions.

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

### Import a topic to the knowledge base category

Use importTopic to import a topic into the knowledge base.

```javascript
importTopic(topicId, options)
```

* topicId - The source topic ID.
* options - An object to specify optional behavior. Available options are
  * update: KB topic ID - Update an existing KB topic instead of creating a new one.
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

## Installation

Install from the Git repository.

https://github.com/37Rb/discourse-chatbot-kb-tools.git
