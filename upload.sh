port=/dev/ttyUSB0

cd bus-departures-cli

for pyfile in *.py;
do
    echo Uploading $pyfile...
    ampy -p $port put $pyfile
done
