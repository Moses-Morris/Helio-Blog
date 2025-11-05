from website import create_app

if __name__ == "__main__":
    blogapp = create_app()
    blogapp.run(debug=True) 