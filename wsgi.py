from app import application

if __name__ == "__main__":
    application.run(port=os.environ["PORT"])