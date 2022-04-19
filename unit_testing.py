import unittest
import final_project as fp

class TestCard(unittest.TestCase):

    def test_tree(self):

        self.assertEqual(fp.tree.children[0].data, 'Deli')
        self.assertEqual(fp.tree.children[1].data, 'Coffee and Tea')
        self.assertEqual(fp.tree.children[2].data, 'Deserts')
        self.assertEqual(fp.tree.children[3].data, 'American')
        self.assertEqual(fp.tree.children[4].data, 'Healthy')
        self.assertEqual(fp.tree.children[5].data, 'International')
        self.assertEqual(fp.tree.children[6].data, 'Bars')
        self.assertEqual(fp.tree.children[7].data, 'Mediterranean and Seafood')

        # Deli category
        self.assertEqual(fp.tree.children[0].children[0].data, 'Bakeries')
        self.assertEqual(fp.tree.children[0].children[1].data, 'Sandwiches')
        self.assertEqual(fp.tree.children[0].children[2].data, 'Delis')
        self.assertEqual(fp.tree.children[0].children[3].data, 'Bagels')

        

        # Coffee and Tea category
        self.assertEqual(fp.tree.children[1].children[0].data, 'Coffee & Tea')
        self.assertEqual(fp.tree.children[1].children[1].data, 'Tea Rooms')
        self.assertEqual(fp.tree.children[1].children[2].data, 'Cafes')
        self.assertEqual(fp.tree.children[1].children[3].data, 'Coffee Roasteries')

        # Deserts category
        self.assertEqual(fp.tree.children[2].children[0].data, 'Gelato')
        self.assertEqual(fp.tree.children[2].children[1].data, 'Macarons')
        self.assertEqual(fp.tree.children[2].children[2].data, 'Ice Cream & Frozen Yogurt')
        self.assertEqual(fp.tree.children[2].children[-1].data, 'Patisserie/Cake Shop')

        # American category
        self.assertEqual(fp.tree.children[3].children[0].data, 'Breakfast & Brunch')
        self.assertEqual(fp.tree.children[3].children[1].data, 'Middle Eastern')
        self.assertEqual(fp.tree.children[3].children[2].data, 'Hot Dogs')

        # Healthy category
        self.assertEqual(fp.tree.children[4].children[0].data, 'Gluten-Free')
        self.assertEqual(fp.tree.children[4].children[1].data, 'Vegetarian')
        self.assertEqual(fp.tree.children[4].children[2].data, 'Juice Bars & Smoothies')
        self.assertEqual(fp.tree.children[4].children[-1].data, 'Soup')

        # International category
        self.assertEqual(fp.tree.children[5].children[0].data, 'Africa')
        self.assertEqual(fp.tree.children[5].children[1].data, 'Asia')
        self.assertEqual(fp.tree.children[5].children[2].data, 'Latin America')
        self.assertEqual(fp.tree.children[5].children[3].data, 'Europe')
        self.assertEqual(fp.tree.children[5].children[4].data, 'Canada')

        # Africa category
        self.assertEqual(fp.tree.children[5].children[0].children[0].data, 'Moroccan')
        self.assertEqual(fp.tree.children[5].children[0].children[1].data, 'African')
        self.assertEqual(fp.tree.children[5].children[0].children[-1].data, 'Ethiopian')

        # Asia category
        self.assertEqual(fp.tree.children[5].children[1].children[0].data, 'Asian Fusion')
        self.assertEqual(fp.tree.children[5].children[1].children[1].data, 'Indian')
        self.assertEqual(fp.tree.children[5].children[1].children[2].data, 'Vietnamese')
        self.assertEqual(fp.tree.children[5].children[1].children[-1].data, 'Dim Sum')

        # Bars category
        self.assertEqual(fp.tree.children[6].children[0].data, 'Beer Bar')
        self.assertEqual(fp.tree.children[6].children[1].data, 'Cocktail Bars')
        self.assertEqual(fp.tree.children[6].children[2].data, 'Wine Bars')
        self.assertEqual(fp.tree.children[6].children[3].data, 'Breweries')
        self.assertEqual(fp.tree.children[6].children[-1].data, 'Tiki Bars')



if __name__=="__main__":
    unittest.main(verbosity=2)