#!/usr/bin/env python3
from passlib.context import CryptContext


def main():
    passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = input("Enter a password: ")
    print("Hashed Password: ", passwordContext.hash(password))


if __name__ == "__main__":
    main()
