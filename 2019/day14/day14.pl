#use strict;
use warnings;
use Data::Dumper;

my $DBG = 1;
my @input;
my $file = shift or die "input missing";
open(my $fh, '<', "$file");
my %lookup = ();

while (my $row = <$fh>) {
	chomp $row;
	#print "$row\n" if $DBG;
	$row =~ /(.+) => (\d+) (\w+)/;
	my @parts = split /,/, $1;
	my $le = @parts;
	my $vc = $2;
	my $vn = $3;
	#print "[ $vc of $vn :: $le]\n" if $DBG;
	push @input, $row;

	if (not exists $lookup{$vn}) {
		$lookup{$vn} = {};
	}
	my $totallen = keys %lookup;
	#print " $vn :: $totallen\n" if $DBG;
	foreach ( @parts ) {
		my $k = $_;
		$k =~ /(\d+) (\w+)/;
		my $c = $1 + 0;
		my $n = $2;
		#print " : $vn : $n = $c , $vc\n" if $DBG;
		my %foo;
		$foo{'yield'} = $vc;
		$foo{'cost'}  = $c;
		$lookup{$vn}->{$n} = \%foo;
	}
}

sub ppo
{
	my (%needs) = @_;
	my $sk;
	print "---------------------\n";
	for $sk (sort(keys %needs)) {
		print "|$sk : $needs{$sk}\n" unless ($sk eq 'FUEL' or $sk eq 'ORE');
	}
	print "|FUEL : $needs{'FUEL'}\t";
	print "|ORE  : $needs{'ORE'}\n";
	print "---------------------\n";
}

sub check
{
	my (%needs) = @_;
	my $sk;
	my $notzero = 0;
	for $sk (sort(keys %needs)) {
		if ($sk ne 'ORE' and $needs{$sk} > 0) {
			++$notzero;
		}
	}
	return $notzero > 0;
}

#print "-------\n";
#print @input;
#print "\n-------\n";
print Dumper(\%lookup);
#print Dumper(%lookup{'FUEL'});
print "-------\n";
my %needs;
for ( keys %lookup ) {
	$needs{$_} = 0;
}
$needs{'ORE'} = 0;
$needs{'FUEL'} = 1;
#print Dumper(\%needs);
#print "-------\n";
ppo %needs;

my $loops = 0;
while (check(%needs)) {
    ++$loops;
	#last if ($loops > 12);
	#ppo %needs;

	foreach my $k (keys %needs) {
		next if ($needs{$k} <= 0 or $k eq 'ORE');

		my $v = $lookup{$k};
		my $res = 0;
		foreach my $k2 (keys %$v) {
			#print "$k => $k2 => ";
			#print $v->{$k2}->{'yield'};
			#print " for ";
			#print $v->{$k2}->{'cost'};
			#print "\n";
			$needs{$k2} += $v->{$k2}->{'cost'};
			$res = $v->{$k2}->{'yield'};
		}
		$needs{$k} -= $res;
	}
}
ppo %needs;
print "$loops iterations\n";
