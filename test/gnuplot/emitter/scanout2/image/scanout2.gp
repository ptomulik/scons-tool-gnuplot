set terminal png;
set output "scanout2_1.png"; # First output
plot sin(x);
set output 'scanout2_2.png' # Second output
plot cos(x); # set output "fake1.png";
# set output 'fake2.png'
set output "scanout2_3.png" ; ;; ;
plot tan(x);

# vim: set syntax=gnuplot expandtab tabstop=4 shiftwidth=4 nospell:
