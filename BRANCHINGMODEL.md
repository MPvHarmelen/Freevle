# Branching model

We use the branching model described in [an excellent article](http://nvie.com/posts/a-successful-git-branching-model/). Most of the article can be summarized in a single image, but it's definitely required to read it (it's not very long or hard to read) before starting development, or your pull requests will be denied by default.

So, here's a short summary of the branch types:

* `master`  
 Only stable releases will be on this branch, which means that anyone cloning the repository will automatically get a stable release to build their templates and such on. The releases will be tagged with their respective version number.
* `develop`  
 Full time development. Anything that will definitely be in the next release should be in here. That means no large added features!
* `release-` branches  
 Branched off from the `develop` branch, these are ready-for-release bugfix-only branches. It's branched off from `develop` when the necessary features are there, then massively tested.
* `feature-` branches  
 This is important, because this is where we steer away from the original article. Branches starting with `feature-` are planned features, but not necessarily for the next release. That means: no experimental "I just thought of this"-features, nothing specific to your own school.
* `hotfix-` branches  
 These are branched off from `master`, shouldn't be too much of these. Fixing major bugs in apparently-not-so-stable releases. Major bugs *only*.

The exact ways to create each branch are discussed in the article, although I think most of it is just your basic branching.

And here's the same thing explained in a more visual form:

![A successful git branching model](http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png)
