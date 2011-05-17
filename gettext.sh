#!/bin/sh

usage="\
Usage: $0 <extract|update|compile>

Extract or compile gettext messages."

if [ -z "$1" ]; then
    echo "$usage"
elif [ $1 == "extract" ]; then
    echo "Extracting messages into the POT template…"
    pybabel extract -F configs/babel.cfg -o tzos/translations/messages.pot tzos/ -c l10n -k _l
elif [ $1 == "update" ]; then
    echo "Updating languages from the latest template…"
    pybabel update -i tzos/translations/messages.pot -d tzos/translations/
elif [ $1 == "compile" ]; then
    echo "Compiling translations…"
    pybabel compile -d tzos/translations/
else
    echo "Unrecognized option."
    echo
    echo "$usage"
fi
