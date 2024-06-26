from library_system import Book,add_book,InvalidISBNException
import unittest

##############
# not c1 or c2 or not c3
# c1: book.isbn is string 
# c2: length of isbn isn't 13
# c3: book.isbn is digit
##############

class TestAddBook(unittest.TestCase):
    #initialize library as a dictionary first
    def setUp(self):
        self.library = dict()
    
    #c1, c2, c3 is defined as above, Note that c2 is defined as "length of isbn isn't 13"


    # testcase1: c1 == true, c2 = false, c3 = true
    def testcase1(self):
        book = Book("Title1", "Author1", "1234567890123")
        add_book(self.library, book)
        #not c1 or c2 or not c3 == false, no exception, book added!
        self.assertIn("1234567890123", self.library)

    # testcase2: c1 == false, c2 = true, c3 = false (since isdigit is a function for string) 
    def testcase2(self):
        book = Book("Title2", "Author2", 10)
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
        self.assertNotIn(10, self.library)

    # testcase3: c1 == true, c2 = true, c3 = false       
    def testcase3(self):
        book = Book("Title3", "Author3", "a")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
        self.assertNotIn("a", self.library)
    
    # testcase4: c1 == true, c2 = false, c3 = false       
    def testcase4(self):
        book = Book("Title4", "Author4", "aaaaaa12aaaaa")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
        self.assertNotIn("aaaaaa12aaaaa", self.library)

    # testcase4: c1 == true, c2 = true, c3 = true  
    def testcase5(self):
        book = Book("Title5", "Author5", "123456789") 
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
        self.assertNotIn("123456789", self.library)





if __name__ == '__main__':
    unittest.main()
