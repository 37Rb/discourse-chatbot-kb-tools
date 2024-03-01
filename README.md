# Discourse Chatbot Knowledge Base Tools
Knowledge base management tools for Discourse Chatbot

Discourse Chatbot is an AI chatbot plugin for Discourse that can be used to make a support bot on your forum. Visit [Meta](https://meta.discourse.org/t/discourse-chatbot-now-smarter-than-chatgpt/256652) and [Github](https://github.com/merefield/discourse-chatbot) to learn more about it.

Discourse Chatbot uses [RAG](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts) to provide the AI model with domain-specific knowledge of your forum. While it's possible to let the bot access every public post on your forum, it may be benficial to limit access to a specific, non-public "knowledge base" category where you curate only high-quality posts that you want the bot to see.

Discourse Chatbot semantic-searches the forum for individual posts instead of topics which makes it challenging for the bot to find complete questions and answers. Often the question/problem is in one post while the answer/solution is in a later post. There may even be multiple back and forth posts leading up the the answer. The topic title and tags may also be useful to the bot but aren't included in this search because it's limited to posts.

Chatbot Knowledge Base Tools help you import knowledge from your forum & website into the knowledge base category in a format the bot to find and use. For example, you can:

* Import entire topics into the knowledge base as a single post so that the bot can see the entire conversation with all relevent context.
* Import pages from your website into the knowledge base so the bot can use them in addition to your forum content.

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

* types: Array of import types - The types to update. Defaults to all.

It's recommended to use await with updateAllImports() so that you can see when it's done.

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

Install from the Git repository.

https://github.com/37Rb/discourse-chatbot-kb-tools.git

ImportWebPage needs to access resources on other domains. You need to configure [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) and [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) to allow it.

Configure [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) by in Discourse admin *content security policy script src* setting (found under Security). Add https://unpkg.com/turndown/dist/turndown.js as a script source so that [Turndown](https://github.com/mixmark-io/turndown) can be loaded.

Configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) by adding an [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) HTTP header to the website you will import from allowing your Discourse forum origin (https:// and domain name) to access content on that website. Alternatively, you can disable CORS checks in your browser when importing web pages.