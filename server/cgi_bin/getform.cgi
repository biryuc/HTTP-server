#!/bin/bash

echo "Content-type: text/html"
echo ""

echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Form </title>'
echo '</head>'
echo '<body>'

echo '<h2> Registration form </h2>'
  echo "<form method=\"GET\" action=\"${SCRIPT}\">"\
       '<table nowrap>'\
          '<tr><td>First Name: </TD><TD><input type="text" name="firstname" value="" ></td></tr>'\
          '<tr><td>Last Name: </td><td><input type="text" name="lastname" value=""></td>'\
          '</tr></table>'


  echo '<br><input type="submit" value="Process Form">'

  if [ "$REQUEST_METHOD" != "GET" ]; then
        echo "<hr>Script Error:"\
             "<br>Usage error, cannot complete request, REQUEST_METHOD!=GET."\
             "<br>Check your FORM declaration and be sure to use METHOD=\"GET\".<hr>"
        exit 1
  fi

  if [ -z "$QUERY_STRING" ]; then
        exit 0
  else
     # No looping this time, just extract the data you are looking for with sed:
     fn=`echo "$QUERY_STRING" | sed -n 's/^.*firstname=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
     ln=`echo "$QUERY_STRING" | sed -n 's/^.*lastname=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

     echo "First name: " $fn >> ../log.txt
     echo "Last name: " $ln >> ../log.txt
  fi
echo '</body>'
echo '</html>'

exit 0