==================
Graphorrhea Design
==================
Mostly pending

User Storage
============

Need to be able to log users in so randos on the internet cant see my notes

* Separately from git repo
* In external server
* In git -- gross

Option 1: Separately from git repo
----------------------------------

e.g. in a sqlite3 or zodb database

* Pros
    - Keeps things separate from notes
    - Each instance which shares notes would have to have its own user database
* Cons
    - Each instance which shares notes would have to have its own user database (Or sync databases)

Option 2: In external server
----------------------------
e.g. in PostgreSQL

* Pros
    - Keeps things separate from notes
    - It's Postgres what could go wrong
* Cons
    - Additional service to setup (would be nice to not need external server)

This is actually probably option 1, since if I go with SQLite, I will probably use an
ORM, so switching to an external server would be easy if I go that route.

Option 3: Inside git repo
-------------------------

* Pros
    - I mean I guess syncing would be able to share users
* Cons
    - Users would be version controlled
    - It's gross, and everytime the repo is published you'd also be publishing users
    - Big design goal is to just be able to publish notes with minimal cruft

Note metadata
=============

Reasoning
---------

Notes need to have metadata with them for ACL, to do things like prevent users from
editing other users notes. Currently since there are two formats I want to support
(MarkDown and ReStructuredText) there are also two ways to pass this metadata:

Markdown metadata with YAML frontmatter:

.. code-block:: markdown

    ---
    author: nick
    created: "2021-03-15T08:00:00Z"
    modified: "2021-03-15T08:09:00Z"
    ---
    This is the **markdown** section

ReStructuredText metadata with docinfo frontmatter [1]_:

.. code-block:: rst

    :author: nick
    :created: 2021-03-15T08:00:00Z
    :modified: 2021-03-15T08:09:00Z

    ============================
    This is the ReStructuredText
    ============================
    :author: also another author, this is not part of the frontmatter


Using a docinfo block for ReStructuredText seems like a pretty good idea. but I dont
seem to be able to parse a RST document, strip out / add the docinfo, and write a RST
document, so I'd have to write my own writer, which I dont want to do.

I'll probably stick with the YAML FrontMatter for both markdown and rst since thats
pretty simple.

Fields
------

* Author
    - for access control
    - Would be nice if this isnt attached to the user id
    - Possible formats:
        - UUID
            - doesn't allow for users to move between instances with their data
            - meaningless outside of system
        - username
            - maintains meaning outside of system
            - forces usernames to be immutable
* Created/Modified date
    - Nice to have, probably not necessary
* Format
    - maybe mimetype? text/markdown, text/x-rst, etc...?
    - Probably useless, but might be necessary if the user is using a format we dont support

.. [1] Like Sphinx_ does
.. _Sphinx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#file-wide-metadata