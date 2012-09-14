Coding Guidelines
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

