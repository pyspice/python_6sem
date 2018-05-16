from bottle import run, route, template
import os

def get_books(author):
	return os.listdir('books/' + author + '/')	

@route('/author/<author>/book/<name>/')
def get_book(author, name):
	fin = open('books/' + author + '/' + name, 'r', encoding='utf-8')
	book = fin.read()
	fin.close()
	return template('book', text=book)

def get_authors():
	return os.listdir('books/')

@route('/author/<author>/')
def get_author_page(author):
	return template('books', books=get_books(author), author=author)

@route('/')
def main():
	authors = get_authors()
	books = {author: get_books(author) for author in authors}
	return template('authors', authors=authors, books=books)

run(host='localhost', port=10666)