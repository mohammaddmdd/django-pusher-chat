# One-to-one private chat using Pusher Channels, Django and Vue.js -

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This application uses the following:

- [Python 3.10+](https://www.python.org/)
- [Node.js](https://nodejs.org/) version 18.0 or above
- [Vue cli](https://cli.vuejs.org/guide/installation.html)

### Setting up the project

First, clone this repository to your local machine:

```sh
 $ git clone 
```

Next, update the following keys in the `api/.env` file with your correct Pusher keys:

```
PUSHER_APP_ID=app_id
PUSHER_KEY=key
PUSHER_SECRET=secret
PUSHER_CLUSTER=cluster
```

Then, update the `.env` file in the project’s root folder with your correct Pusher App key:

```
    VUE_APP_PUSHER_KEY=<PUSHER_APP_KEY>
    VUE_APP_PUSHER_CLUSTER=<PUSHER_APP_CLUSTER>
```

### Running the Apps

#### Run the Flask app

- CD to the Django folder - api:

```
    $ cd api/chatappProject
```

- Create a virtual environment:

```
python3 -m venv env
```

- Activate the virtual environment:

```
  source env/bin/activate
```

On windows? Activate it with the below:

```
  source env/Scripts/activate
```


- Download NLTK corpora:

$ python -m textblob.download_corpora lite

- Finally run the app:

```
 flask run
```

Check the URL where Flask is running - [http://localhost:8000](http://localhost:8000).

#### Run the Vue app

Open a new terminal window, then cd into the projects root folder - `one-to-one chat`:

Install dependencies:

```
npm install
```

Then run the app:

```
    $ npm run serve
```

## Built With

- [Django](https://djangoproject.com/) - A framework for Python
- [Pusher](https://pusher.com/) - APIs to enable devs building realtime features
- [Vue.js](https://vuejs.org/) - A JavaScript Framework for building User Interfaces