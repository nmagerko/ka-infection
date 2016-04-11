# Infection

### Purpose

This project models student-teacher relationships between users for Khan Academy's "Infection" interview challenge. These relationships are used to simulate the appropriate infection of users with certain versions of a software build.

### Implementation Overview
`User` instances act like nodes in a graph. Each of these instances belongs to a `Classroom`, which acts as an implicit container for connected components (merging with other classrooms as needed). The `UserAcademy` acts as a container for all users (by way of containing their classrooms), and provides the overall infection functionality.

### Getting Started

##### Installation
Clone this project into a directory on your machine. You will need Python 2.7.x, but no packages need to be installed.

##### Testing
Tests are provided in a `tests.py` file at the root of this project. Each test is commented with the functionality it tests. To see their output, run

```
python tests.py
```

from the root of this project.

##### Usability
A `main.py` file is provided with the imports needed to start playing around with the project already there. All classes have their constructors and mutator methods commented to make their purposes/effects easier to understand.

These classes can be found in the `users` subdirectory of this project. Note that all classes (excluding the UserAcademy) also have their `__str__` and `__repr__` methods overridden, so you can print out your users as you model them.

##### Warning
I did not have time to make my `User` class immutable. However, it is crucial that no relationships are added to any users that have been used to create a `UserAcademy`, or the `limited_infection` methods may malfunction.
