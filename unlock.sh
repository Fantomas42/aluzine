dbus-monitor --session "type='signal',interface='com.ubuntu.Upstart0_6'" | \
    (
	while true; do
	    read X
	    if echo $X | grep "desktop-unlock" &> /dev/null; then
		aluz-in;
	    fi
	done
    )