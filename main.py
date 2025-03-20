
from app import create_app

main = create_app()

if __name__ == '__main__':
    main.run(host="0.0.0.0", port=5000)