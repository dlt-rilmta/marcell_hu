#! /bin/bash

TESTDIR=$(mktemp -d /tmp/dtestXXXXXX)
FNAME='trv_mk11151_2011clxxvii'

date >$TESTDIR/log

# CLI
cat test/${FNAME}.txt | \
docker run -i --rm mtaril/marcell_hu:test annotate >${TESTDIR}/${FNAME}.conllup 2>>${TESTDIR}/log

# echo ${TESTDIR}

DIFF=$(git diff --no-index --color-words test/${FNAME}.conllup ${TESTDIR}/${FNAME}.conllup)

if [ -z "$DIFF" ] ; then
    echo 'Docker CLI test passed.' ;
else
    echo -e "$DIFF"
    echo "Docker CLI test failed, see the $TESTDIR/ directory."
    exit 1
fi

# REST
docker run --name marcell_test -p 5000:5000 --rm -d mtaril/marcell_hu:test
curl -F "file=@test/${FNAME}.txt" localhost:5000/annotate >${TESTDIR}/${FNAME}.conllu
docker container stop marcell_test

DIFF=$(git diff --no-index --color-words test/${FNAME}.conllup ${TESTDIR}/${FNAME}.conllup)

if [ -z "$DIFF" ] ; then
    echo 'Docker REST test passed.' ;
else
    echo -e "$DIFF"
    echo "Docker REST test failed, see the $TESTDIR/ directory."
    exit 1
fi
