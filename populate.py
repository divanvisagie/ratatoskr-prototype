from repositories.user import NewUser, UserRepository

def main():
    repo = UserRepository()
    user = NewUser("DivanVisagie", 0)
    repo.save(user)

if __name__ == '__main__':
    main()

