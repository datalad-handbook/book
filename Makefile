.PHONY: build clean-ml clean-neuro2 clean-neuro clean-provenance clean-collaboration clean-usecases clean-beyond_basics clean-basics clean
build: html
SHELL := /bin/bash

# this pattern rule lets you run "make build" (or any other target
# in docs/Makefile) in this directory as though you were in docs/
%:
	$(MAKE) -C docs $@

clean-build:
	rm -rf docs/_build 

# wipe out everything
clean:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs -name _examples -type d | xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@for d in $$(git grep ':workdir:' -- docs | cut -d ':' -f 4- | sort | uniq|cut -d '/' -f 1 | uniq); do chmod +w -R /home/me/$$d; rm -vrf /home/me/$$d ; done
	# wipe out bare push repos
	@chmod +w -R /home/me/pushes; rm -vrf /home/me/pushes
	@rm -vrf /home/me/makepushtarget.py
	# wipe out the RIA store
	@rm -vrf /home/me/myriastore
	# wipe out the DVC comparison
	@chmod +w -R /home/me/DVCvsDL; rm -vrf /home/me/DVCvsDL

# remove the Basics
clean-basics:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/basics/_examples -name 'DL*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@for d in $$(git grep ':workdir:' -- docs | cut -d ':' -f 4- | sort | uniq|cut -d '/' -f 1 | uniq | sed 's/usecases//' | sed 's/DVCvsDL//' | sed 's/beyond_basics//'); do chmod +w -R /home/me/$$d; rm -vrf /home/me/$$d ; done
	# wipe out bare push repos
	@chmod +w -R /home/me/pushes/DataLad-101 /home/me/pushes/midterm_project; rm -vrf /home/me/pushes/DataLad-101 /home/me/pushes/midterm_project
	@rm -vrf /home/me/makepushtarget.py

# remove Beyond-Basics
clean-beyond_basics:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/beyond_basics/_examples -name 'DL*' |xargs rm -vrf
    # also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/beyond_basics; rm -vrf /home/me/beyond_basics
	# wipe out bare push repos
	@chmod +w -R /home/me/pushes/data-version-control; rm -vrf /home/me/pushes/data-version-control
	# wipe myriastore
	@rm -vrf /home/me/myriastore

# remove all usecases
clean-usecases:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'DL*' |xargs rm -vrf
    # also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases; rm -vrf /home/me/usecases

# remove all challenges
clean-challenges:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/challenges/_examples -name 'cha*' |xargs rm -vrf
    # also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/challenges; rm -vrf /home/me/challenges


# remove specific usecases
clean-collaboration:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'collab*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases/collab; rm -vrf /home/me/usecases/collab

clean-provenance:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'prov*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases/provenance; rm -vrf /home/me/usecases/provenance

clean-neuro:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'repro-*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases/repro; rm -vrf /home/me/usecases/repro

clean-neuro2:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'repro2*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases/repro2; rm -vrf /home/me/usecases/repro2

clean-ml:
	# check if we have something like .xsession or a .bashrc
	@[ -n "$$(ls -a /home/me/.x* /home/me/.*rc 2>/dev/null)" ] && echo "/home/me looks like a real HOME dir. Refusing to bring chaos" && exit 1 || true
	@find docs/usecases/_examples -name 'ml*' |xargs rm -vrf
	# also wipe the workdirs, otherwise a rebuild will lead to chaos
	@chmod +w -R /home/me/usecases/{ml-project,imagenette}; rm -vrf /home/me/usecases/{ml-project,imagenette}
