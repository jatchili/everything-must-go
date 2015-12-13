# everything-must-go

This is a Django web app for auctioning off items to the highest bidder. It's useful if you're moving and you need to get rid of stuff.

There's no mechanism for payment processing - the app merely notes how much each bidder is supposed to pay. So, you should only use it among people you trust to pay their debts.

## Setup

### Settings

First, copy `emg/settings-example.py` to `emg/settings.py`. (The latter file is gitignored, because it'll be different in development vs. production.) Then, you can go through and modify the settings in `emg/settings.py`:

* `SECRET_KEY`: Some long random string. Don't disclose the key used in production, or else all sorts of Bad Things™ will happen.
* `DEBUG`: Set this to `True` in development if you want to debug errors.
* `ALLOWED_HOSTS`: You can replace this with a domain if you want to prevent the app from being accessed from any other domain.
* `BASE_URL`: If the app is hosted on a non-root path (e.g. `www.example.com/mysite`), then this should be the path, surrounded by slashes (`/mysite/`).

### If your domain contains an underscore

There's an annoying "[bug](https://code.djangoproject.com/ticket/19952)" in Django: If `DEBUG` is set to `False`, and your domain contains an underscore, then your site won't work in production even it works locally. You can fix this as follows:

1. Locate the Django installation running on your production server, by running `python`, and issuing the Python commands `import django` and `django.__file__`. The output (minus the `__init__.pyc` at the end) will tell you where your Django installation is stored. `cd` into that directory.
2. Open `http/request.py` in your favorite text editor.
3. Find the line beginning with `host_validation_re = re.compile` (currently [line 25](https://github.com/django/django/blob/b0c56b895fd2694d7f5d4595bdbbc41916607f45/django/http/request.py#L25)).
4. In that line, replace `[a-z0-9.-]` with `[a-z0-9.-_]`

(This isn't specific to this app, but I'm documenting it here because I was really confused by this.)

### Running the app

This is standard Django stuff:

Initialize the database with `python manage.py migrate`. Create an admin account with `python manage.py createsuperuser`.

To run locally for development, do `python manage.py runserver` and open http://127.0.0.1 in a browser.

There's not much I can say about how to run it in production, since each host will have a different procedure for deploying Django apps.

## Using the site

### Adding items

There's no real interface for adding items for sale. To do this, first log in using the credentials you created in the `createsuperuser` step, and then go to the URL `/admin`. Next to "Items", click "Add". Fill in the fields, and then save the item.

"Image url" should point to an image of the item. (There's no facility for uploading images, so you should host them on a site like [Imgur](http://imgur.com).) "Ask" is the minimum bid allowed, which must be a multiple of $0.25. "Category" should be exactly one of: `books clothing toys office household food`. (If you want to change the list of categories, you'll need to edit the template at `templates/main/index.html`.)

### Running the auctions

There's no email required to sign up, so you should ask people who sign up to tell you their username by some means (email, in person, etc.), so that you can contact them if they win stuff.

Bids must be in multiples of $0.25. The price listed on top of the image is the price that new bidders have to beat, and the price that the winner would pay if bidding were to close right now. If two bids are tied for highest, then the earliest one wins.

It's important that bidders understand: If there are two or more bids, the listed price is just $0.25 plus the second-highest bid. **This means that you don't need to constantly one-up the last bid by $0.25 whenever a bid is made until you're unwilling to bid further.** Instead, you should just bid the most you're willing to pay. The result will be the same as if you had employed this strategy.

Of course, this means that you, the admin, have a responsibility to keep the actual bids secret, and to refrain from participating yourself. (The bids are listed in a table on each item's page, but only when you're logged in as the superuser.) Otherwise, people will lose trust in the system, and revert to the "increment by $0.25" strategy, and it'll generally be annoying for everyone.