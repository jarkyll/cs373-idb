
FILES :=                       \
    models.html                \
    IDB1.log                   \
    app/models.py              \
	app/tests.py 			   \
	dn_init.sql				   \
    manage.py                  \
    IDB1.log                   \
    app/demo/__init__.py       \
	app/tests.py 			   \
    UML.pdf                    \
    unit_models.py


ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint
endif

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

models.html: app/models.py
	pydoc3 -w app/models.py

IDB2.log:
git log > IDB2.log

pylint_mtests: .pylintrc 
-$(PYLINT) app/models.py
-$(PYLINT) app/tests.py


TestModels.tmp:
	$(COVERAGE) run --omit='*sqlalchemy*' --branch app/tests.py > TestModels.tmp 2>&1
	$(COVERAGE) report -m                 >> TestModels.tmp
	cat TestModels.tmp

check:
		@not_found=0;                             \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
	echo "success";


clean:
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  models.html
	rm -f  models.log
	rm -rf __pycache__


format:
	autopep8 -i app/models.py
	autopep8 -i app/tests.py
	autopep8 -i app/demo/__init__.py
	autopep8 -i manage.py
	autopep8 -i unit_models.py


status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: models.html IDB2.log format pylint_mtests check TestModels.tmp



