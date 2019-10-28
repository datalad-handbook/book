.PHONY: build clean-examples
build: html

# this pattern rule lets you run "make build" (or any other target
# in docs/Makefile) in this directory as though you were in docs/
%:
	cd docs && make $@

# wipe out all recorded examples
clean-examples:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs -name _examples -type d | xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@for d in $$(git grep ':workdir:' -- docs | cut -d ':' -f 4- | sort | uniq | cut -d '/' -f 1 | uniq); do chmod +w -R /home/me/$$d; rm -vrf /home/me/$$d ; done
