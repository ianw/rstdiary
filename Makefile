rpm:
	spectool -C ~/rpmbuild/SOURCES/ -g python-rstdiary.spec
	rpmbuild -ba python-rstdiary.spec
