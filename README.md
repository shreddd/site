Software Carpentry Website
==========================

This repository holds the source for
the [Software Carpentry](http://software-carpentry.org) website.
Home pages for bootcamps are not stored in this repository:
if you want to create one,
please see the instructions in the `bc repository.

Contributing
------------

Software Carpentry is an open source/open access project,
and we welcome contributions of all kinds.
By contributing,
you are agreeing that Software Carpentry may redistribute your work
under [these licenses](http://software-carpentry.org/license.html).

Software Carpentry uses a development workflow similar to that of [AstroPy](http://astropy.org)
and many other open source projects.
The AstroPy docs have excellent sections on:

*   [Getting started with Git](http://astropy.readthedocs.org/en/latest/development/workflow/index.html#getting-started-with-git)
*   [Developer workflow](http://astropy.readthedocs.org/en/latest/development/workflow/development_workflow.html)

What You Need to Clone
----------------------

This repository is roughly 145 MBytes in size
(roughly half of which is image files in the blog).
The Version 3 and Version 4 lesson materials are stored in submodules
because they are 20 and 600 MBytes respectively,
and people who only want to add blog posts don't need them.
When you clone this repository,
empty subdirectories called `v3` and `v4` are created to hold the submodules.
You do not need to `git update` these in order to build the miscellaneous pages and blog,
though the links in `_site/*` to these files won't resolve properly if they are not present.

Building
--------

Building the website requires [Jekyll](http://jekyllrb.com/),
which we use to compile templated HTML pages,
and [Python](http://python.org/),
which we use for pre- and post-processing.
We use Jekyll because it's what [GitHub](http://github.com/) uses;
we use Python because most of our volunteers speak it.

*   Type `make` to see a list of all available commands.
*   Type `make check` to build everything in `_site` for testing.
    (Depending on your machine, this takes about 10-15 seconds.)

Blogging 
--------

To create a new blog post:

1.  Fork this repository on GitHub, and clone that to your desktop.
2.  Create a file `blog/YYYY/MM/post-name.html`,
    where `YYYY` is a four-digit year and `MM` is a two-digit month.
3.  Fill in the metadata at the top of the file:
    -   `layout` *must* be `blog`.
    -   `author` must be an author identifier like `wilson.g`.
        See `standard_config.yml` in repo's root directory for a list of author identifiers,
        and contact the Software Carpentry administrators if you need to be added.
    -   `title` is the post title.
    -   `date` the date of the post (in YYYY-MM-DD format).
    -   `time` must be an HH:MM:TT clock time.
        Use 09:00:00 for the first post on a particular day,
        10:00:00 for the second,
        and so on,
        so that posts can be ordered.
    -   `category` must be a list of category identifiers.
        See `standard_config.yml` in repo's root directory for a list of categories,
        and contact the Software Carpentry administrators if you want to add a new one.
4.  Use HTML to write the post.
    -   Use `<!-- start excerpt -->` and `<!-- end excerpt -->`
        to mark a paragraph or two at the start
        as the excerpt to show in feed readers.
    -   If you need to refer to our email address, it is `{{page.contact}}`.
    -   If you need to another post, or something else on the site, use `{{page.root}}/path/to/file`.
    -   We also provide `{{site.site}}` (the base URL for the site),
        `{{site.twitter_name}}`,
        `{{site.twitter_url}}`,
        `{{site.facebook_url}}`,
        `{{site.google_plus_url}}`,
        and `{{site.rss_url}}`
        (all of which should be self-explanatory).
5.  Please add any images your blog post needs to the same blog/YYYY/MM directory as the post itself.
    Please use lower-case names without special characters for image files.
6.  `make` in the root directory will list available commands;
    `make check` will rebuild the web site in the `_site` directory.
    Open `_site/index.html` to see your post on the blog's home page,
    `_site/blog/index.html` to see it on the blog home page,
    and `_site/YYYY/MM/post-name.html` to see the post itself.
7.  When you're satisfied with your post,
    `git add path/to/post` and `git commit -m "Adding a blog post about something or other"`
    will commit it to your local copy (on your laptop).
8.  `git push origin master` will push it to your clone on GitHub
    (assuming you've added your fork on GitHub as a remote called `origin`).
9.  Go to GitHub and issue a pull request from your clone to `swcarpentry/website`,
    then assign it to `@gvwilson` or `@amyrbrown` for proof-reading.

Design Notes
------------

The images used in this site are divided between the `img` and `assets` directories.
The former is a duplicate of the `bc` repository's `img` directory,
while the latter contains files that are only used in the website.
The `img` files are duplicated because the alternatives are all complicated:

1.  We want to keep the `bc` module 
    (which instructors use as a starting point for bootcamp home pages)
    as simple as possible,
    which rules out a submodule for images.
2.  Clever tricks with symbolic links proved fragile in practice,
    and meant that include files in the `bc` and `site` repositories
    had to use different paths to refer to shared images.

In addition:

*   The `css` and `js` directories in `bc` and `site` are duplicates,
    for the same reasons given above.
*   Some of the material in the `_includes` directory
    is duplicated in the `bootcamp` template repository,
    but only some.
*   We generate our own RSS feed (in `feed.xml`) and blog home page
    because Jekyll insists on using `_posts/YYYY-MM-DD-name.html`,
    and we don't want to have hundreds of files in one directory.
*   Bootcamp pages for old bootcamps
    are stored in the `bootcamps` directory of this repository,
    since there's little point in creating repos for them.
    New bootcamps should be created using the process described earlier.
