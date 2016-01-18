Cookiepatcher
=============

Tool to apply updates of cookiecutter templates for projects.

Don't you think it's hard to follow changes of cookiecutter templates?

Usage
-----

To apply changes of `audreyr/cookiecutter-pypackage`, type like this at your project repository::

    cookiepatcher

And specify cookiecutter template and revisions to apply::

    Input template repository url: gh:audreyr/cookiecutter-pypackage
    Input template version applied currently: 5a519e6f19655468332ff95990bb7d107571061c
    Input version to follow [master]: master


Or you can specify from arguments::

    cookiepatcher --template gh:audreyr/cookiecutter-pypackage --diff 5a519e6f19655468332ff95990bb7d107571061c master


From the second time
--------------------

Cookiepatcher will create `cookiepatcher.json` config file.
If you have this file on the repository root,  cookiepatcher won't ask you anything
(template url, revisions, variables).
It will apply patches to follow `master` of the cookiecutter template.
