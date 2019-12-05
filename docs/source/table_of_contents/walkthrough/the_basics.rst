=========================
The Basics
=========================

These are the instructions to get you ready to run the code.

If you're not a super-noob like I was a couple months ago,
you might want to skip this section.


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

**Then, you'll need Python and a package manager.**

I recommend Anaconda.

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

Also ensure you have a way to download packages, e.g. ``numpy``.

For example, this is how to install ``numpy`` using Anaconda
(I already had it downloaded, but it updated some stuff)::

    (base) [callum@cedar5 Nmax8]$ conda install numpy
    Collecting package metadata (current_repodata.json): done
    Solving environment: -
    done

    ## Package Plan ##

    environment location: /home/callum/.local/easybuild/software/2017/Core/miniconda3/4.3.27

    added / updated specs:
        - numpy


    The following packages will be downloaded:

        package                    |            build
        ---------------------------|-----------------
        ca-certificates-2019.11.27 |                0         132 KB
        certifi-2019.11.28         |           py37_0         156 KB
        ------------------------------------------------------------
                                            Total:         288 KB

    The following packages will be UPDATED:

    ca-certificates                              2019.10.16-0 --> 2019.11.27-0
    certifi                                  2019.9.11-py37_0 --> 2019.11.28-py37_0


    Proceed ([y]/n)? y


    Downloading and Extracting Packages
    certifi-2019.11.28   | 156 KB    | ########################################################################################################### | 100%
    ca-certificates-2019 | 132 KB    | ########################################################################################################### | 100%
    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    (base) [callum@cedar5 Nmax8]$

All good up to here?

**Now do yourself a favour and download these programs.**

You don't have to, but I've found them helpful.

1. `Visual Studio Code <https://code.visualstudio.com/>`_

- It's a good editor on it's own, so it's recommended on that front,
  but the real power is in the extensions.
- Install the ``Remote - SSH`` extension and you'll be able to edit/run code
  on remote machines as if they were local.
- The downside to this is that it can refuse to connect sometimes, which
  means you'll be stuck with the terminal or something while it's down.

2. If you're on a mac, `Cuberduck <https://cyberduck.io/>`_

- It makes transfering / viewing remote files a whole lot nicer.

3. Again for mac users, `XQuartz <https://www.xquartz.org/>`_

- This lets you see remote files like plots without having to download them
- If you're not on a mac, you'll want some other X11 forwarding software



Let's Download That Code
--------------------------------

Follow these steps::

    (base) callum@itheory10 ~ % cd /path/where/i/want/to/put/files/called/dir/
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
