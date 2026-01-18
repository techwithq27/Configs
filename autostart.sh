#!/usr/bin/env bash

run() { command -v "$1" >/dev/null 2>&1 && "$@" & }


run xrandr --output HDMI-1 --mode 3440x1440 --rate 60 --primary --output eDP-1 --off
run variety
#run flatpak run com.notesnook.Notesnook
run pgrep -x xss-lock >/dev/null || xss-lock --transfer-sleep-lock -- i3lock -n -c 000000 &
#run /usr/libexec/polkit-kde-authentication-agent-1
#run klipper
#run kdeconnect-indicator
#run nm-applet

# Autostart applications for Qtile

# Start Variety for wallpapers
# variety &

# # Start Notesnook (Flatpak)
# flatpak run com.notesnook.Notesnook &

# # Start CopyQ for clipboard management
# #copyq &

# /usr/libexec/polkit-kde-authentication-agent-1 &
# klipper &
# kdeconnect-indicator &
# nm-applet &


