# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Clove
SOURCEDIR     = docs
BUILDDIR      = docs_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


clean:
	rm -rf $(BUILDDIR)


gh-pages:
	git checkout gh-pages
	rm -rf *
	git checkout master $(SOURCEDIR)
	git reset HEAD
	sphinx-build $(SOURCEDIR) $(BUILDDIR)
	mv -fv $(BUILDDIR)/* ./
	rm -rf $(SOURCEDIR) $(BUILDDIR)
	git add -A
	git ci -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master


livehtml:
	sphinx-autobuild -b html $(SOURCEDIR) $(BUILDDIR)/html -B -z clove


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
