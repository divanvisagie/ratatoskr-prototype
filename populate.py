from repositories.user import NewUser, UserRepository

def main():
    try:
        repo = UserRepository()
        user = NewUser("DivanVisagie", 0)
        repo.save(user)
        print("User saved")
    except Exception as e:
        print(e)       

if __name__ == '__main__':
    main()

