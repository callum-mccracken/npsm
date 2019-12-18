.. _basics:

=================================
The Basics
=================================

These are the instructions to get you ready to run the code.

Before We Download the Code
--------------------------------

It's worth taking a second to discuss some preliminaries before jumping into
the code.

**First, make sure you have a computer.**

Then make sure it's not running Windows.

I suppose if you want to use Windows, you should be fine, but nothing's been
tested on there, so use at your own risk.

**Make sure you have git installed.**

Enter ``git`` in a terminal, and see if you get a bunch of help text.

If so, you're good.

If not, fix that.

**Then, you'll need Python and Anaconda.**

- If you're on a local machine, download it from `here <https://www.anaconda.com/distribution/>`_
  - Here's a `quickstart guide <https://docs.anaconda.com/anaconda/user-guide/getting-started/>`_
- If you're using a computecanada machine, follow `these instructions <https://docs.computecanada.ca/wiki/Anaconda/en>`_ instead

However you choose to get it, ensure you are now running Python
(the latest version of course, currently that's 3.7.4).

You should see something like this when you run Python::

    (base) callum@itheory10 docs % python
    Python 3.7.4 (default, Aug 13 2019, 15:17:50)
    [Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Now you can just create a conda environment with all required packages::

    conda env create -f environment.yml

If somehow you're unable to use Anaconda and have to manually install
packages like a caveman, this should be a complete list of what you'll need::

    matplotlib v. 3.1.1
    numpy v. 1.17.2
    scipy v. 1.3.1

And these last 3 are only necessary if you want to edit the docs::

    sphinx v. 2.2.0
    m2r v. 0.2.1
    sphinx-rtd-theme v. 0.4.3


**Now do yourself a favour and download these programs.**

You don't have to, but I've found them helpful.

1. `Visual Studio Code <https://code.visualstudio.com/>`_

- It's the `most popular editor in the world <https://insights.stackoverflow.com/survey/2019#technology-_-most-popular-development-environments>`_ as of 2019, for good reason.
- If you install the ``Remote - SSH`` extension, you'll be able to edit/run
  code on remote machines as if they were local.

2. If you're on a mac, `Cuberduck <https://cyberduck.io/>`_

- It makes transfering / viewing remote files a whole lot nicer.

3. Again for mac users, `XQuartz <https://www.xquartz.org/>`_

- This lets you see remote files like plots without having to download them
- If you're not on a mac, you'll want some other X11 forwarding software



Now Let's Download That Code
--------------------------------

Follow these steps::

    (base) callum@itheory10 ~ % cd /i/want/to/put/files/in/this/dir/
    (base) callum@itheory10 dir %
    (base) callum@itheory10 dir % git clone https://github.com/callum-mccracken/npsm.git
    Cloning into 'npsm'...
    remote: Enumerating objects: 1488, done.
    remote: Counting objects: 100% (1488/1488), done.
    remote: Compressing objects: 100% (845/845), done.
    remote: Total 1488 (delta 913), reused 1182 (delta 608), pack-reused 0
    Receiving objects: 100% (1488/1488), 9.14 MiB | 1.96 MiB/s, done.
    Resolving deltas: 100% (913/913), done.
    (base) callum@itheory10 dir % cd npsm
    (base) callum@itheory10 npsm % ls

You have now downloaded the code, and you should be set up to run it!

In each of the folders you see in the npsm directory, there are scripts
to help you with different calculations.
