# Add noise to .wav or .flac files

Programm takes 3 arguments:
- input directory -- directory with sounds
- noise directory -- directory with noise sounds, one of them would be chosen randomly
- power -- power of noise in range [0.01 : 0.2]

hw1 ./example ./beeps 0.1

As a result a new directory would be created with name "[input_directory]_noised", where the structure and all the files whould be the same as in input directory. All the .flac  and .wav files whould be noised.
