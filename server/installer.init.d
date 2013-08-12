#!/bin/sh
# chkconfig: 345 98 05
PIDFILE=/var/run/installer/uwsgi.pid
UWSGI=/usr/bin/uwsgi
CONFIG=/work/installer/app/installer-uwsgi.xml
OUT_LOG=/var/log/installer/uwsgi-out.log
#LD_LIBRARY_PATH=:/usr/lib/oracle/11.2/client64/lib/

RUN="${UWSGI} --pidfile=${PIDFILE} -d ${OUT_LOG} ${CONFIG}"

. /etc/init.d/functions

case "$1" in
        start)
                if [ -f $PIDFILE ] ; then
                        echo_failure "UWSGI is already running"
                        exit 0
                fi
                $RUN
                sleep 3
                if ps `cat $PIDFILE` >/dev/null 2>&1 ; then
                        echo "Started"
                else
                        echo "Failed to start"
                fi
        ;;
        stop)
                if [ -f $PIDFILE ] ; then
                        kill -INT `cat $PIDFILE`
                        echo -n "Stopping "
                        while [ -x $PIDFILE ] ; do
                                echo -n '.'
                                sleep 1
                        done
                        echo
                        sleep 1
                        echo "Stopped"
                else
                        echo "${PIDFILE} not found"

                fi
        ;;
        restart)
                $0 stop
		sleep 8
                $0 start
        ;;
        *)
                N=/etc/init.d/$NAME
                echo "Usage: $N {start|stop|restart}" >&2
                exit 1
                ;;
esac


