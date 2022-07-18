#! /bin/sh
module=$1
rate=$2
echo "PyLint: Checking changes!"
code_rate=$(pylint --disable=E0401 $module | grep "rated at" | awk '{print $7}' | sed -e 's|/[0-9,]*||g')
if (( $(echo "$code_rate > $rate" |bc -l) )); then
    echo "PyLint: Code Rate $code_rate"
    echo "PyLint: Looks good"
    exit 0
else
  echo "PyLint: This is bad code"
  pylint $module
  exit 1
fi
done