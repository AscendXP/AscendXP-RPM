#!/bin/sh

if [ "$(id -u)" -eq 0 ]; then
    echo "Error: Do not run $0 as root or with sudo!" >&2
    echo "This script must be executed as your normal user account." >&2
    exit 1
fi

ASAR_HASH="INSERT_HASH_HERE"
CHANNEL=stable
DOWNLOAD=https://updates.discord.com/
DIR=discord
EXE=Discord
PKG_NAME="equicord"
SHARE_DIR="/usr/share/$PKG_NAME"
BOOTSTRAP_SUFFIX="$PKG_NAME/updater_bootstrap"

config_home=$XDG_CONFIG_HOME
if [ -z "$config_home" ]; then
    config_home=$HOME/.config
fi

discord_host=$config_home/$DIR/$EXE

if [ ! -x "$discord_host" ]; then
    mkdir -p "$config_home/$DIR"
    if [ ! -d "$config_home/$DIR" ]; then
        echo "Fatal error, failed to create $DIR in $config_home" >&2
        exit 1
    fi
    if [ -t 1 ]; then
        zenity=--no-zenity
    else
        zenity=--zenity
    fi
    bootstrap=/usr/share/$BOOTSTRAP_SUFFIX
    if [ ! -x "$bootstrap" ]; then
        bootstrap=/opt/$BOOTSTRAP_SUFFIX
        if [ ! -x "$bootstrap" ]; then
            bootstrap="$(dirname -- "$0")/updater_bootstrap"
        fi
    fi

    app_dir=$("$bootstrap" $zenity "$config_home/$DIR" $CHANNEL "$DOWNLOAD")
    if [ "$?" = "0" ]; then
        echo "Bootstrap complete"
        ln -fs "$config_home/$DIR/$app_dir/$EXE" "$discord_host"
        exec "$0" "$@"
    else
        echo "Bootstrap failed or was canceled"
        exit 2
    fi
fi

DISCORD_ROOT="$(dirname "$(readlink -f "$discord_host")")"
RESOURCES="$DISCORD_ROOT/resources"

mkdir -p "$RESOURCES"

(
    cd "$RESOURCES" || exit 1

    if [ ! -f equicord.asar ]; then
        cp "$SHARE_DIR/equicord.asar" ./equicord.asar
    fi

    CURRENT_HASH=""
    if [ -f app.asar ]; then
        CURRENT_HASH=$(sha256sum app.asar | awk '{ print $1 }')
    fi

    if [ "$ASAR_HASH" != "$CURRENT_HASH" ]; then
        if [ -f app.asar ] && [ ! -f _app.asar ]; then
            mv app.asar _app.asar
        fi
        cp "$SHARE_DIR/app.asar" ./app.asar
    fi
)

exec "$discord_host" "$@"
