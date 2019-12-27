#use strict;
use warnings;
use Data::Dumper;
use POSIX qw/ceil/;
use Storable qw(dclone);

my $DBG = 1;
my @input;
my $file = shift or die "input missing";
my $fuel_in = shift or die "fuel missing";
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
	my ($ore, %needs) = @_;
	my $sk;
	print "---------------------\n";
	for $sk (sort(keys %needs)) {
		print "|$sk : $needs{$sk}\n" unless ($sk eq 'ORE');
	}
	print "|ORE  : $ore\n";
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
#print Dumper(\%lookup);
#print "-------\n";

sub calc_ore
{
	my ($fuel_in, %lookup) = @_;
	my %needs;
	my %extra;
	my $ore = 0;
	for ( keys %lookup ) {
		$extra{$_} = 0;
	}
	my $tmpf = $lookup{'FUEL'};
	foreach my $k (keys %$tmpf) {
		$needs{$k} = $fuel_in * $lookup{'FUEL'}->{$k}->{'cost'};
	}
	#ppo($ore, %needs);

	my $loops1 = 0;
	my $loops2 = 0;
	my $loops3 = 0;
	while (check(%needs)) {
	    ++$loops1;
		my %post;

		foreach my $k (keys %needs) {
		    ++$loops2;

			if ($extra{$k} > $needs{$k}) {
				$extra{$k} -= $needs{$k};
				next;
			} else {
				$needs{$k} -= $extra{$k};
				$extra{$k} = 0;
			}

			my $v = $lookup{$k};
			my $res = 0;

			foreach my $k2 (keys %$v) {
				++$loops3;
				$res  = $v->{$k2}->{'yield'};
				$cost = $v->{$k2}->{'cost'};
				$nq = ceil($needs{$k} / $res) * $cost;
				$eq = $nq / $cost * $res - $needs{$k};
				if (not exists($post{$k2})) {
					$post{$k2} = 0;
				}
				$post{$k2} += $nq;
			}
			$eq = $nq / $cost * $res - $needs{$k};
			if ($eq ne 0) {
				$extra{$k} += $eq;
			}
		}
		if (exists($post{'ORE'})) {
			$ore += $post{'ORE'};
		}
		delete($post{'ORE'});
		%needs = %post;
	}
	#ppo($ore, %needs);
	#print "$loops1 iterations\n";
	#print "$loops2 iterations\n";
	#print "$loops3 iterations\n";
	return $ore;
}

sub part2
{
	my (%lookup) = @_;
	$ore = calc_ore(1, %lookup);
	my $tri = 1000000000000;
	my $low = int($tri / $ore);
	$high = $low * 2;
	my $y = $low * $ore;
	$r = 0;

	while ($low <= $high) {
		$h = int( ($low + $high) / 2);
		$r = calc_ore($h, %lookup);
		#print "T $tri\n";
		#print "R $r\n";
		#print "L $low\n";
		#print "H $high\n";
		if ($r < $tri) {
			$low = $h + 1;
		}
		if ($r > $tri) {
			$high = $h - 1;
		}
	}
	return $high;
}

$ore = calc_ore($fuel_in, %lookup);
$fuel = part2(%lookup);

print "\nPart 1: $ore\n";
print "\nPart 2: $fuel\n";
