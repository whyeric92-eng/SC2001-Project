# SC2001 Project 1: Integration of Merge Sort & Insertion Sort

Course project for SC2001 (Algorithm Design and Analysis).

Implements a hybrid sorting algorithm that switches from Merge Sort to
Insertion Sort once a subarray's size drops to or below a threshold `S`,
then empirically studies the number of key comparisons and CPU time across
different input sizes `n` and threshold values `S`, comparing against plain
Merge Sort.
