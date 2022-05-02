# STACKS - Social Media Tracker, Analyzer, & Collector Toolkit at Syracuse (v2.0)
STACKS (v 2.0) is the updated version of the previous [STACKS interface](https://github.com/bitslabsyr/stack). As of April 2021, STACKS v2.0 has been leveraged with its latest Python v3.9, along with its updated Mongo and PyMongo dependencies. The social media research toolkit was originally designed to collect, process, and store data from online social networks, majorly from social media APIs such as Twitter and Facebook. The interface is an ongoing project via the Syracuse University iSchool, and the following repository supports the Twitter search and pagination API. Collecting from the Facebook search and pagination API is under development.

**_This documentation assumes the following:_**
* You know how to use Ubuntu 20.04.
* You know how to use ssh.
* Your server has MongoDB, Docker and Docker Compose already installed.
* You understand how to edit files using vim (“vi”) or nano.
* You have rights and know how to install Python libraries.


## Installation

Prior to installing STACK, make sure you have MongoDB, Docker and Docker Compose installed and running on your server.

* Install MongoDB on Ubuntu 20.04: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
* Install Docker on Ubuntu 20.04: https://docs.docker.com/engine/install/
* Install Docker Compose on Ubuntu 20.04: https://docs.docker.com/compose/install/


## Steps on how to use it

The STACKS documentation contains a collector tool by the name of _abcd.py_. Upon opening it, we change the search the following query parameter:
```
"query_parameters": {
            "query": "from:<Insert the Twitter User ID here>",
            "expansions": "author_id",
            "tweet.fields": ["author_id", "conversation_id", "created_at", "geo", "id",
                             "public_metrics", "promoted_metrics", "organic_metrics",
                             "in_reply_to_user_id", "referenced_tweets", "source", "text"],
            "user.fields": ["created_at", "description", "entities", "id", "location",
                            "name", "pinned_tweet_id", "url", "username"],
            "media.fields": ["media_key", "preview_image_url", "type", "url",
                             "public_metrics", "organic_metrics", "promoted_metrics", "alt_text"]
        },
```
Hit run and keep the code running until desired time. The data starts getting stored in the MongoDB database accordingly.

## Credits

Lovingly maintained at Syracuse University by:

* [Jeff Hemsley](https://github.com/jhemsley)
* [Jonathan Stromer-Galley](https://github.com/jstromergalley)
* [Hrishikesh Telang](https://github.com/hrishitelang)
* [Yiran Duan](https://github.com/yiran-duan)


Distributed under the MIT License:

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
