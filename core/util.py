# -*- coding: utf-8 -*-

def dict_key_slice(d, size):
	i = 1
	s = []
	for k in d.iterkeys():
		s.append(k)
 		if i == size:
 			yield s
			i = 1
			s = []
		else:
			i += 1
	if s:
		yield s


def list_slices(l, size):
	i = 0	
	while l:
		s = l[i:i+size]
		yield s
		l = l[i+size:]


