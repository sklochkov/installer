%define _builddir	.
%define _sourcedir	.
%define _specdir	.
%define _rpmdir		.

Name:		iqbuzz-installer-modules
Version:	0.1
Release:	11

Summary:	IQBuzz installer master package
License:	Proprietary
Group:		System Environment/Libraries
Distribution:	Red Hat Enterprise Linux

BuildArch:	noarch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
IQBuzz installer master package

%package server
Summary:        IQBuzz installer server module
License:        Proprietary
Group:          System Environment/Daemons
Distribution:   Red Hat Enterprise Linux
BuildArch:      noarch
Requires:	python
Requires:	MySQL-python
Requires:	uwsgi-plugin-python = 0.9.8.6-1.el6
Requires:	nginx
Requires:	python-flask

%description server
IQBuzz installer server module

%prep


%build


%install
%{__rm} -rf %{buildroot}
install -d -m755 %{buildroot}/work/installer/app/templates/
install -d -m755 %{buildroot}/work/installer/html/static/images/
install -d -m755 %{buildroot}/usr/share/installer/
install -d -m755 %{buildroot}/etc/init.d
install -d -m755 %{buildroot}/etc/installer
install -d -m755 %{buildroot}/etc/nginx/conf.d/
install -d -m755 %{buildroot}/var/log/installer/
install -d -m755 %{buildroot}/var/run/installer/
install -d -m755 %{buildroot}/var/log/nginx/installer

cd server/
install -m644 config.py %{buildroot}/work/installer/app/config.py
install -m644 installer.conf %{buildroot}/etc/installer/installer.conf
install -m755 installer.init.d %{buildroot}/etc/init.d/installer
install -m644 installer-nginx.conf %{buildroot}/etc/nginx/conf.d/installer.conf
install -m644 installer_server_app.py %{buildroot}/work/installer/app/installer_server_app.py
install -m644 installer_server.py %{buildroot}/work/installer/app/installer_server.py
install -m644 installer.sql %{buildroot}/usr/share/installer/installer.sql
install -m644 installer-uwsgi.xml %{buildroot}/work/installer/app/installer-uwsgi.xml
install -m644 my_exceptions.py %{buildroot}/work/installer/app/my_exceptions.py
install -m644 profile_manager.py %{buildroot}/work/installer/app/profile_manager.py
install -m644 repo_manager.py %{buildroot}/work/installer/app/repo_manager.py

install -m644 static/jquery-ui.css %{buildroot}/work/installer/html/static/jquery-ui.css
install -m644 static/jquery-ui.js %{buildroot}/work/installer/html/static/jquery-ui.js
install -m644 static/jquery.js %{buildroot}/work/installer/html/static/jquery.js
install -m644 static/images/ui-bg_highlight-soft_100_eeeeee_1x100.png %{buildroot}/work/installer/html/static/images/ui-bg_highlight-soft_100_eeeeee_1x100.png
install -m644 static/images/ui-bg_highlight-soft_75_ffe45c_1x100.png %{buildroot}/work/installer/html/static/images/ui-bg_highlight-soft_75_ffe45c_1x100.png
install -m644 static/images/ui-icons_ffffff_256x240.png %{buildroot}/work/installer/html/static/images/ui-icons_ffffff_256x240.png
install -m644 static/images/ui-icons_ef8c08_256x240.png %{buildroot}/work/installer/html/static/images/ui-icons_ef8c08_256x240.png
install -m644 static/images/ui-bg_glass_100_fdf5ce_1x400.png %{buildroot}/work/installer/html/static/images/ui-bg_glass_100_fdf5ce_1x400.png
install -m644 static/images/ui-icons_222222_256x240.png %{buildroot}/work/installer/html/static/images/ui-icons_222222_256x240.png
install -m644 static/images/ui-bg_diagonals-thick_18_b81900_40x40.png %{buildroot}/work/installer/html/static/images/ui-bg_diagonals-thick_18_b81900_40x40.png
install -m644 static/images/ui-bg_diagonals-thick_20_666666_40x40.png %{buildroot}/work/installer/html/static/images/ui-bg_diagonals-thick_20_666666_40x40.png
install -m644 static/images/ui-icons_228ef1_256x240.png %{buildroot}/work/installer/html/static/images/ui-icons_228ef1_256x240.png 
install -m644 static/images/ui-bg_flat_10_000000_40x100.png %{buildroot}/work/installer/html/static/images/ui-bg_flat_10_000000_40x100.png
install -m644 static/images/ui-bg_glass_65_ffffff_1x400.png %{buildroot}/work/installer/html/static/images/ui-bg_glass_65_ffffff_1x400.png
install -m644 static/images/ui-icons_ffd27a_256x240.png %{buildroot}/work/installer/html/static/images/ui-icons_ffd27a_256x240.png
install -m644 static/images/ui-bg_gloss-wave_35_f6a828_500x100.png %{buildroot}/work/installer/html/static/images/ui-bg_gloss-wave_35_f6a828_500x100.png
install -m644 static/images/ui-bg_glass_100_f6f6f6_1x400.png %{buildroot}/work/installer/html/static/images/ui-bg_glass_100_f6f6f6_1x400.png
install -m644 static/images/animated-overlay.gif %{buildroot}/work/installer/html/static/images/animated-overlay.gif
install -m644 static/custom.css %{buildroot}/work/installer/html/static/custom.css

install -m644 templates/header.html %{buildroot}/work/installer/app/templates/header.html
install -m644 templates/profile_list.html %{buildroot}/work/installer/app/templates/profile_list.html
install -m644 templates/footer.html %{buildroot}/work/installer/app/templates/footer.html
install -m644 templates/profile_form.html %{buildroot}/work/installer/app/templates/profile_form.html
install -m644 templates/kickstart.cfg %{buildroot}/work/installer/app/templates/kickstart.cfg
install -m644 templates/configuration.html %{buildroot}/work/installer/app/templates/configuration.html 
install -m644 templates/scripts_and_styles.html %{buildroot}/work/installer/app/templates/scripts_and_styles.html



%clean
rm -rf $RPM_BUILD_ROOT

%post

%files server
%defattr(-,root,root)
%dir %attr(0755,root,root) /work/installer/
%dir %attr(0755,root,root) /var/log/installer/
%dir %attr(0755,root,root) /var/run/installer/
%dir %attr(0755,root,root) /var/log/nginx/installer
%attr(0755,root,root) /etc/init.d/installer
%attr(0644,root,root) /etc/installer/installer.conf
%attr(0644,root,root) /etc/nginx/conf.d/installer.conf
%attr(0644,root,root) /usr/share/installer/installer.sql
%attr(0755,root,root) /work/installer/app/*
%attr(0755,root,root) /work/installer/html/static/*



