# -*- coding: utf-8 -*-

def f7(seq):
	"""
	Make the list unique. called f7 because unique is a reserved word
	"""
	seen = set()
	seen_add = seen.add

	return [ x for x in seq if x not in seen and not seen_add(x)]