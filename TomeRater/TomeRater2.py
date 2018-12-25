#! python3
# RBA: Roger B. Atkins, rba2124@gmail.com
# Cohort-nov-27-2018

# Tome Rater Project

# Note: At first I coded a 4 'star' rating system, but when
# I started adding books that I have read, I felt compelled
# to convert it to a 5 'star' system.


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}    # book: rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return print("User's email address has been updated.")
        # Changes user's email; print('User's email has been updated.')

    def __repr__(self):
        bks_read = 0
        for book in self.books:
            bks_read += 1
        return 'User {name}, email: {email}, books read: {num_bks_read}'.format(name=self.name, email=self.email, num_bks_read=bks_read)

    def __eq__(self, other_user):
        if self.name == other_user and self.email == other_user.email:
            return print('The users are the same.')

    def read_book(self, book, rating='None'):
        self.books[book] = rating

    def __hash__(self):
        return hash((self.name, self.email))

    def get_average_rating(self):
        total = 0.0
        if self.books == {}:
            return 0
        else:
            for rating in self.books.values():
                if rating != 'None' and rating != '' and rating != 0:
                    total += float(rating)
        return round(total / len(self.books), 2)


class Book():    # Why no author?
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        return print('ISBN has been updated.')

    def add_rating(self, rating):
        if rating != 'None' and float(rating) > 0 and float(rating) <= 5:
            self.ratings.append(rating)
        else:
            return print("Invalid Rating")

    def __eq__(self, other_book):
        if self.isbn == other_book.isbn and self.title == other_book.title:
            return print('The books are the same.')

    def get_average_rating(self):
        total = 0.0
        for rating in self.ratings:
            if rating != 'None' and rating != '':
                total += float(rating)
        return round(total / len(self.ratings), 2)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return 'Book object: {title}, ISBN: {isbn}'.format(title=self.title, isbn=self.isbn)


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return ('{title} by {author}'.format(title=self.title, author=self.author))


class Non_Fiction(Book):    # Why no author?
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject    # type str
        self.level = level        # type str

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return ('{title}, a {level} manual on {subject}'.format(title=self.title, level=self.level, subject=self.subject))


class TomeRater():
    def __init__(self):
        self.users = {}    # email:user
        self.books = {}    # book:num users who read it

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating='None'):
        if email not in self.users.keys():
            return print('No user with email ' + email +'!')
        else:
            self.users[email].read_book(book, rating)
            if rating != 'None':
                book.add_rating(rating)
            if book not in self.books.keys():
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books='None'):
        if email not in self.users.keys():
            self.users[email] = User(name, email)
        if user_books != 'None' and user_books != '' and user_books != []:
            for book in user_books:
                self.add_book_to_user(book, email, )

    def print_catalog(self):
        print('\nCatalog:\n')
        if len(self.books) == 0:
            print('There are no catalogued books.')
        for key in self.books.keys():
            if type(key) == Book:
                print(key.title + ', ISBN: ' + str(key.isbn))
            else:
                print(key)
        return print()

    def print_users(self):
        user_list = []
        for value in self.users.values():
            user_list.append(value)
        print('\nUser List:\n')
        for user in user_list:
            print(user)
        return print()

    def most_read_book(self):
        most = 0
        mr_books = {0: {}}
        for book, reads in self.books.items():
            if most == 0 and mr_books[0] == {}:
                most = reads
                mr_books[0] = {book: most}
            else:
                if reads > most:
                    most = reads
                    mr_books[0] = {book: most}
        # Test for ties:
        for book, reads in self.books.items():
            if reads == most and book not in mr_books[0].keys():
                mr_books[0][book] = reads
        print('\nMost Read Book(s):\n')
        for book, reads in mr_books[0].items():
            print('{book} read by {reads}'.format(book=book, reads=reads))
        return ''

    def highest_rated_book(self):
        high_average = 0
        hi_aver_bks = {0: {}}
        for key in self.books.keys():
            ave_rating = key.get_average_rating()
            if ave_rating > high_average:
                high_average = ave_rating
        for key in self.books.keys():
            ave_rating = key.get_average_rating()
            if ave_rating == high_average:
                hi_aver_bks[0][key] = ave_rating
        print('\nHighest Rated Book(s):\n')
        for book, ave in hi_aver_bks[0].items():
            print('Title: {book} Average Rating: {ave}'.format(book=book, ave=ave))
        return ''

    def most_positive_user(self):
        hi_rating = 0.0
        hi_users = {0:{}}
        mpu = []    # Most Positive User(s)
        for user in self.users.values():
            av_rating = user.get_average_rating()
            if av_rating > hi_rating:
                if hi_rating == 0 and hi_users[0] == {}:  # mpu == []:
                    hi_rating = av_rating
                    # mpu.append(user)
                    hi_users[0] = {user: hi_rating}
                else:
                    hi_rating = av_rating
                    hi_users[0] = {user: hi_rating}

        # Test for ties:
        for user in self.users.values():
            if user.get_average_rating() == hi_rating and user not in hi_users[0].keys():
                hi_users[0] += {user: hi_rating}
        for user in hi_users[0].keys():
            average = hi_users[0][user]
            return '\nMost Positive User(s): {user} Average Rating: {average}'.format(user=user, average=average)


Tome_Rater = TomeRater()

# Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
print(book1)    # Test __repr__ for Book object.
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
print(nonfiction1)    # Test __repr__() for Non_Fiction object.
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)
print(novel3)    # Test __repr__() for Fiction object.
get_prog = Tome_Rater.create_non_fiction("Get Programming: Learn to Code With Python", "Python", "beginner", 9781617293788)
smart_pyth = Tome_Rater.create_non_fiction("A Smarter Way to Learn Python", "Python", "beginner", 1010101010999)
silent = Tome_Rater.create_novel("The Silent Corner", "Dean Koontz", 9780345546784)

# Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")
Tome_Rater.add_user("Roger B. Atkins", "rba2124@gmail.com")

# Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

# Add book to user:
Tome_Rater.add_book_to_user(get_prog, "rba2124@gmail.com", 4.5)
Tome_Rater.add_book_to_user(nonfiction1, "rba2124@gmail.com", 4.7)
Tome_Rater.add_book_to_user(smart_pyth, "rba2124@gmail.com", 4.5)
Tome_Rater.add_book_to_user(silent, "rba2124@gmail.com", 4.2)

# Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

# Test functions/methods:
Tome_Rater.print_catalog()
Tome_Rater.print_users()

# print("Most positive user:")
print(Tome_Rater.most_positive_user())
# print("Highest rated book:")
print(Tome_Rater.highest_rated_book())
# print("Most read book:")
print(Tome_Rater.most_read_book())


def again():
    again = ''
    while again == '' or (again != 'n' and again != 'y'):
        again = input('Another? (y/n)').lower()
    return again

def book4list():
    book = ''
    while book == '':
        book = input('Enter book title: ').title()
    return book


def add_user():
    name = ''
    another = ''
    user_books = []
    while name == '':
        name = input('Enter name of user: ').title()
    email = ''
    while email == '' or '@' not in email or (
            '.com' not in email and '.edu' not in email and
            '.org' not in email):
        email = input("Enter valid e-mail address for user: ")
    more = ''
    while more == '' or (more != 'y' and more != 'n'):
        more = input('Include list of books user has read? (y/n) ').lower()
    book = ''
    if more == 'y' and another != 'n':
        while another != 'n':
            user_books.append(book4list())
            another = again()
        Tome_Rater.add_user(name, email, user_books=user_books)
    else:
        Tome_Rater.add_user(name, email)


def menu():
    print('\nMain Menu\n')
    print('1. Add User')
    print('2. Add Book')
    print('3. Show User List')
    print('4. Show Catalog')
    print('5. Most Read Book')
    print('6. Highest Rated Book')
    print('7. Add Book to User')
    print('8. Most Positive User')
    print('0. Exit/Quit/Stop')
    ans = ''
    while not ans.isdecimal():
        ans = input('Enter number: ')
    if ans == '1':
        add_user()
    elif ans == '2':

    elif ans == '3':
        print(Tome_Rater.print_users())
    elif ans == '4':
        print(Tome_Rater.print_catalog())
    elif ans == '5':
        print(Tome_Rater.most_read_book())
    elif ans == '6':
        print(Tome_Rater.highest_rated_book())
    elif ans == '7':
        add_bk_2_user()
    elif ans == '8':
        print(Tome_Rater.most_positive_user())
    elif ans == '9':

    elif ans == '1':
    elif ans == '1':
    elif ans == '0':
    print('\nWe hope you enjoyed Tome Rater.')
    print('Have a nice day!')
menu()

# add_user()
