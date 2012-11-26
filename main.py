#!/usr/bin/env python

import life
import detective
from random import randint

WIDTH = 16
HEIGHT = 16
SIZE = WIDTH * HEIGHT

randomdata = [randint(0, 1) for i in range(WIDTH * HEIGHT)]

original = life.Life(WIDTH, HEIGHT, randomdata)
saved = original.clone()

print "Original:"
print original
print

original.tick()
print "Given:"
print original
print

gumshoe = detective.Detective(original)
print "Initial confidence:"
print gumshoe
print

print "Guessing..."
last_span = 0
confidence = 0.0
while gumshoe.span > 1:
    gumshoe.guess(confidence)
    confidence = (confidence + 0.5) / 2.0
    span = gumshoe.span
    if span != last_span:
        print "\t%i" % span
    last_span = span

guess = life.Life(WIDTH, HEIGHT, [a.confidence for a in gumshoe])

print "Guess:"
print guess
print

saved_difference = saved.diff(guess)

guess.tick()
print "Result:"
print guess
print

difference = original.diff(guess)
accuracy = 1.0 - (float(difference) / float(SIZE))

print "Accuracy: %0.3f" % accuracy

saved_accuracy = 1.0 - (float(saved_difference) / float(SIZE))
print "Accuracy to original: %0.3f" % saved_accuracy
