Guidelines
=================

We've put together some guidelines for coding. Keep true to these quasi-rules
or your code will never be accepted into the repo.

In general
----------

* Don't be an idiot. Think before you code.
* Commit plenty!
* Use modern syntax/code/elements/anything. We're living in the twenty-first
  century and we're going to *act* like it.

Python
------

* See PEP 8 for mostly everything.
* Use four spaces. Always. No exceptions. Ever.
* Use single quotes (`'`) not double (`"`).
* One of our goals is personalization, so put everything specific to a certain
  app into the app's folder, where possible. Anything shared may go into `custom`.

HTML
----

Starting with a simple example:

    <div></div>
    <div></div>

    <a href="foo">
      <img src="bar" alt="baz">
    </a>

* Indentation: 2 spaces
* In general, new elements go on new lines.
* If the line gets too long, the closing tag will be on a new line.
* We're writing HTML5, so no `<b>`, `<u>` or `<i>` tags.

CSS
---

Code examples are cool:

    #idelement, .classelement, a:hover {
      color: #F00;
           border-radius: 5px;
      -moz-border-radius: 5px;
      margin: 10px 0 3px 0;
    }

* One space after each colon (`:`).
* If there's vendor-specific prefixes (such as `-webkit` or `-moz`), the value
  sits on the same height.
* Margin and padding on one line, except if you only want to give one side's
  value, like `margin-left`.
* The opening curly bracket (`{`) is seperated *only* by a space from the
  selectors, so no newlines.
* The closing curly bracket is on the same height as the selectors.

Git
---

### Committing: when and how

Since we're using github's issue tracker (found at
https://github.com/Freevle/Freevle/issues), we like to tie our commits to that
as much as possible. So here's a when and how to commit:

#### Commit when...

1. You've fixed an issue.
2. You're working on an issue, but need to work on it further elsewhere.
3. You're working on an issue, but someone else needs to look at it/work on it.

#### Commit how...

Here's an example commit message:

    Made /settings/personal work (#40)

It's a usual Git commit message: no longer than 80 characters, describing what
you did as concise as possible. Then there's the added `(#40)`, this is the
issue number on github's issue tracker. If the commit doesn't complete the
issue - meaning you won't close the issue after committing -, use `(WIP #xx)`,
where xx obviously stands for the issue number.

### Branching model

We use the branching model described in
[an excellent article](http://nvie.com/posts/a-successful-git-branching-model/).
Most of the article can be summarized in a single image, but it's definitely
required to read it (it's not very long or hard to read) before starting
development, or your pull requests will be denied by default.

So, here's a short summary of the branch types:

* `master`  
 Only stable releases will be on this branch, which means that anyone cloning
 the repository will automatically get a stable release to build their
 templates and such on. The releases will be tagged with their respective
 version number.
* `develop`  
 Full time development. Anything that will definitely be in the next release
 should be in here. That means no large added features!
* `release-` branches  
 Branched off from the `develop` branch, these are ready-for-release
 bugfix-only branches. It's branched off from `develop` when the necessary
 features are there, then massively tested.
* `feature-` branches  
 This is important, because this is where we steer away from the original
 article. Branches starting with `feature-` are planned features, but not
 necessarily for the next release. That means: no experimental "I just thought
 of this"-features, nothing specific to your own school.
* `hotfix-` branches  
 These are branched off from `master`, shouldn't be too much of these. Fixing
 major bugs in apparently-not-so-stable releases. Major bugs *only*.

The exact ways to create each branch are discussed in the article, although I
think most of it is just your basic branching.

And here's the same thing explained in a more visual form:

![A successful git branching model](http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png)
