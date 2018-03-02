#!/bin/bash
echo '<!DOCTYPE html>'
echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Form </title>'
echo '</head>'
echo '<body>'

echo '<h2> Registration form </h2>'
  echo '<form method="get">'\
       '<table nowrap>'\
          '<tr><td>First Name: </TD><TD><input type="text" name="firstname" value="" ></td></tr>'\
          '<tr><td>Last Name: </td><td><input type="text" name="lastname" value=""></td>'\
          '</tr></table>'


  echo '<br><input type="submit" value="Process Form">'

echo '</body>'
echo '</html>'

