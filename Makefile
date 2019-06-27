.PHONY: build clean-examples
build: html

# this pattern rule lets you run "make build" (or any other target
# in docs/Makefile) in this directory as though you were in docs/
%:
	cd docs && make $@

# wipe out all recorded examples
clean-examples:
	find docs -name _examples -type d | xargs rm -rf
