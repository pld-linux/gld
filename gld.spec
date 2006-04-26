Summary:	GLD is a standalone greylisting server for Postfix
Summary(pl):	GLD to serwer "szarych list" dla Postfiksa
Name:		gld
Version:	1.6
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.gasmi.net/down/%{name}-%{version}.tgz
# Source0-md5:	95cfe17b92767db4460385972c7f6774
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-conf.patch
URL:		http://www.gasmi.net/gld.html
BuildRequires:	autoconf
BuildRequires:	mysql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gld is a standalone greylisting server for Postfix. It listen on a TCP
port and use MySQL for storing data. The server supports whitelists
based on sender,sender_domain and client_ip. It supports also light
greylisting and DNS white lists.

%description -l pl
GLD to serwer "szarych list" dla Postfiksa. Dane przechowuje w MYSQL,
do komunikacji u¿ywa TCP/IP. Serwer umo¿liwia listowanie bazuj±ce na
NADAWCY, DOMENIE_NADAWCY oraz ADRESIE_IP_CLIENTA. Wspiera równie¿
"light greylisting" i "DNS white lists".

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir}} \
	$RPM_BUILD_ROOT%{_var}/lib/%{name}

# init script:
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install gld $RPM_BUILD_ROOT%{_sbindir}
install gld.conf $RPM_BUILD_ROOT%{_sysconfdir}/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 168 gld
%useradd -u 168 -d %{_var}/lib/%{name} -s /sbin/false -c "GreyListing server for Postfix" -g gld gld

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = 0 ]; then
	%userremove gld
	%groupremove gld
	# should be done?:
	# rm -rf %{_var}/lib/%{name}
fi

%files
%defattr(644,root,root,755)
%doc HISTORY README README-pgsql README-SECURITY tables.mysql tables.pgsql table-whitelist.sql
%attr(640,root,gld) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,gld) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%dir %attr(711,gld,gld) %{_var}/lib/%{name}
