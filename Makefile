.PHONY: git

void:


git:
	git add . 
	git commit -am "Update"
	git push

pypi:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --skip-existing dist/*

