#!/usr/bin/perl

# Server test script
use strict;
use warnings;

use IO::Socket;


my $remote_host="localhost";
my $remote_port="1234";

my $socket = IO::Socket::INET->new("$remote_host:$remote_port");

print $socket "OMG!!!! :-)  Hallo Welt!! Schlecht!\n";
my $line = <$socket>;
print $line."\n";
