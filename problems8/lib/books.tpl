<html>
	<title>The Library 1.0</title>
	<body>
		{{author}}'s books:
		<ul>
		%for book in books:
			<li><a href="/book/{{book}}/">{{book}}</a></li>
		%end
		</ul>
	</body>
</html>