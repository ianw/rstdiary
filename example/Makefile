all: upload-stamp

.PHONY: clean

# note for development you could install from a git checkout too
#  pip install -e ~/path/to/rstdiary
env:
	virtualenv -p python3 env
	./env/bin/pip install rstdiary

output/index.html: env diary.rst diary.cfg
	rm -rf output
	mkdir output
	./env/bin/rstdiary -d diary.cfg
	rm -f upload-stamp

upload-stamp: output/index.html
	touch $@
	$(warning Replace this with an upload command!)
	$(info rsync -avz --delete ./output/ my.server.com:public_html/diary)

clean:
	rm -rf env output upload-stamp

