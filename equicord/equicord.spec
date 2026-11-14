Name:           equicord
Version:        1
Release:        1%{?dist}
Summary:        The other cutest Discord client mod
License:        GPL-3.0-only
URL:            https://equicord.org/
Conflicts:      discord
Source0:        https://discord.com/api/download?platform=linux&format=tar.gz#/discord.tar.gz
Source1:        https://github.com/Equicord/Equicord/releases/download/latest/desktop.asar
Source2:        equicord.desktop
Source4:        equicord.sh
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  hicolor-icon-theme
BuildRequires:  tar
Requires:       libnotify
Requires:       nss
Requires:       gtk3
Requires:       hicolor-icon-theme
AutoReqProv:    no
%global _enable_debug_package 0
%global debug_package %{nil}
%define _build_id_links none

%description
Equicord is the other cutest Discord client mod.

%prep
%setup -q -c -T

mkdir -p discord-bin
tar -xzvf %{SOURCE0} -C discord-bin --strip-components=1
cp %{SOURCE1} desktop.asar

%build
mkdir -p app
echo '{"name": "discord", "main": "index.js"}' > app/package.json
echo 'require(require("path").resolve(require("electron").app.getAppPath(), "..", "equicord.asar"));' > app/index.js

# Use npx to bundle app.asar directly
npx asar pack app app.asar
rm -rf app

HASH=$(sha256sum app.asar | awk '{print $1}')
cp %{SOURCE4} equicord.sh
sed -i "s/INSERT_HASH_HERE/$HASH/" equicord.sh

%install
install -Dm755 equicord.sh %{buildroot}%{_bindir}/%{name}
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -d %{buildroot}%{_datadir}/%{name}

install -m755 discord-bin/updater_bootstrap %{buildroot}%{_datadir}/%{name}/updater_bootstrap
install -m644 app.asar %{buildroot}%{_datadir}/%{name}/app.asar
install -m644 desktop.asar %{buildroot}%{_datadir}/%{name}/equicord.asar

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/

%changelog
