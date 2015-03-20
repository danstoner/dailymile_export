use LWP::UserAgent;
use JSON::PP;
use Text::CSV;
use Getopt::Long;

# use IO::Socket::SSL  # would not build properly but do not need SSL anyway.
#use HTTP::UserAgent;   # requires IO::Socket::SSL for SSL functionality


my $dm_user = "";
my $usage;

#GetOptions....




__END__

#### below this is the cloned perl6 code

# replace this with proper args parsing
if ! @*ARGS[0] {
 say "Usage:\n \n perl6 dailymile_export_to_tsv.p6 dailymile_username";
 exit;
}
if (@*ARGS[0] eq "-h") | (@*ARGS[0] eq "--help") {
 say "\nUsage:\n perl6 dailymile_export_to_tsv.p6 dailymile_username\n\n";
 exit;
}

my $dm_user = @*ARGS[0]; 


my $page = 1;

my $nowtime = DateTime.new(now);
my $nowtimestring = $nowtime.year ~ $nowtime.month ~ $nowtime.day ~ $nowtime.hour ~ $nowtime.minute ~ $nowtime.second;

## try to create output file here
##
##

my $api_url_entries = "http://api.dailymile.com/people/" ~ $dm_user ~ "/entries.json?page=" ~ $page;

say "First API Request: " ~ $api_url_entries;

my $ua = HTTP::UserAgent.new;
my $response = $ua.get($api_url_entries);

if ! $response.is-success {
  die $response.status-line;
} else {

say from-json('{ "a": 42 }').perl;
say to-json { a => [1, 2, 'b'] };

# save this line for now
my %rjson = %(from-json($response.content));


#  my @rjson = %(from-json($response.content)){'entries'};

### Whether I use an array or a hash, from-json seems to be stuffing everything
### into a single element.
#  say "................................................................";

#   for %rjson{@x} {            
#     $_.say;
# }

  

#  my @entries = %(from-json($response.content)){'entries'}[0];
#  my @entries = %(from-json($response.content)){'entries'}[1];
 
#  for @entries {
# #    say $_ => 'id';
#     say $_{'id'};
#     # say "..................";
#     }

}



say "**** Terminating on purpose.***";
exit;
# code below here not used or not ready
