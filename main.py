from app import create_app, post_bp, upload_bp

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)