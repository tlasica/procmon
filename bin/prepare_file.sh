cat $1 | egrep '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' | sed  '1s/^/#/' | sed -e 's/PM//g' -e 's/all//g' -e 's/\,/\./g' -e 's/://g'

