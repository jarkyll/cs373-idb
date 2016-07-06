FILES :=        	\
    .gitignore  	\
    makefile    	\
    apiary.apib 	\
    IDB1.log    	\
    models.html 	\
    app/models.py   \
    app/tests.py    \
    UML.pdf

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
	rm -f  *.pyc
	rm -f  models.html
	rm -f  IDB1.log
	rm -rf __pycache__

format:
	autopep8 -i app/models.py

models.html: app/models.py
	pydoc3 -w models

IDB1.log:
	git log > IDB1.log

