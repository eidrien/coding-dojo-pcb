import unittest
import re

class TestSmilesParsing(unittest.TestCase):
	
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

def parse_smiles_as_tree(smiles):
	m = re.search("^(.+)\((.+)\)(.+)$", smiles)
	if (m):
		return [m.group(1),parse_smiles_as_tree(m.group(2)),m.group(3)]
	return [smiles]
