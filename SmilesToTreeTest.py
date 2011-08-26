import unittest
import re

class TestSmilesParsing(unittest.TestCase):
	
	def test_parsing_smiles_simpliest(self):
		self.assertEqual(['C'], parse_smiles_as_tree('C'))

	def test_parsing_smiles_with_no_branches(self):
		self.assertEqual(['CCCCC'], parse_smiles_as_tree('CCCCC'))

	def test_parsing_smiles_with_one_large_branch(self):
		self.assertEqual([['CCCCC']], parse_smiles_as_tree('(CCCCC)')) 

	def test_parsing_smiles_with_one_branch_in_the_middle(self):
		self.assertEqual(['CC',['CCCCC'],'CO'], parse_smiles_as_tree('CC(CCCCC)CO'))

	def test_parsing_smiles_with_two_main_branches(self):
		self.assertEqual(['Cl',['CCCCCC'],'ZnCO',['Cl'],'CCH'], parse_smiles_as_tree('Cl(CCCCCC)ZnCO(Cl)CCH'))

	def test_nested_branches(self):
		self.assertEqual(['Cl',['CC',['OH'],'CC'],'ZnH'] , parse_smiles_as_tree('Cl(CC(OH)CC)ZnH'))

	def test_not_all_branches_closed_raises_exception(self):
		self.assertRaises(Exception, parse_smiles_as_tree, 'Cl(CC(OH)CCZnH')

	def test_closing_not_opened_branch_raises_exception(self):
		self.assertRaises(Exception, parse_smiles_as_tree, 'ClCC(OH)CC)ZnH')

	def test_empty(self):
		self.assertEqual([], parse_smiles_as_tree(''))

def isatom(a):
	return not a in [ '(' , ')' ]

def parse_smiles_as_tree(smiles):
	return parse_smiles_as_tree_rec(smiles, 0)[0]


def add_branch_to_tree(tree,branch):
	if branch:
		tree.append(branch)

def parse_smiles_as_tree_rec(smiles, level):
	ret = []
	branch =""
	while smiles:
		symbol, smiles = pop_symbol(smiles)
		if isatom (symbol):
			branch += symbol
		elif symbol  == "(":
			add_branch_to_tree(ret, branch)
			branch = ""
			result, smiles = parse_smiles_as_tree_rec(smiles, level +1)
			ret.append(result)
		elif symbol == ")":
			if level == 0:
				raise Exception("branch mismatch")
			add_branch_to_tree(ret, branch)
			return ret, smiles

	add_branch_to_tree(ret, branch)
	if level != 0:
		raise Exception("branch mismatch")
	
	return ret, smiles

def pop_symbol(smiles):
		symbol = smiles[0]
		smiles = smiles[1:]
		return symbol,smiles	
