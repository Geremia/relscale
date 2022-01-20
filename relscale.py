#!/usr/bin/python3

# Automatically scale text up as large as possible to fit within certain page count
# https://tex.stackexchange.com/q/630429/36603

import os, sys

if len(sys.argv) != 4:
    print("Usage example: " + sys.argv[0] + " in.tex max_num_pages tolerance")
    exit()

texinput = sys.argv[1]

s_prev = 0; s = 1 #previous and current scale factor
Δs = float(sys.argv[3]) # tolerance
f = 2 # ∈ (1,∞)
p_max = int(sys.argv[2]) # max number of pages

print("%s\t%s\t%s" % ("relscale", "Δ rescale", "pages"))
while True:
    os.system('sed -i \'s/\\\\relscale{[0-9.]\+}/\\\\relscale{' + str(s) + '}/\' "' + texinput + '"')
    p = int(os.popen('xelatex "'+ texinput + "\" | grep -o '([0-9]\+ pages)' | grep -o '[0-9]\+'").read().strip())
    print("%f\t%f\t%d" % (s, abs(s-s_prev), p))
    if abs(s - s_prev) < Δs and p <= p_max: # break when scale factor s within Δs tolerance
        break
    s_prev = s
    if p <= p_max:
        s *= f
    elif p > p_max:
        s /= f
    f = (1+f)/2
