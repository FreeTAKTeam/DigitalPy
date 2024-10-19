import random

class SecurityController:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        
    def generate_password(length: int, complexity: int) -> str:
        """Generate a password of the specified length and complexity level.

        Parameters:
            length (int): The desired length of the password.
            complexity (int): The desired complexity level of the password.
                0: Only lower case letters.
                1: Lower and upper case letters.
                2: Lower and upper case letters, numbers.
                3: Lower and upper case letters, numbers, special characters.

        Returns:
            str: The generated password.
        """
        # Initialize empty password string
        password = ""

        # Define character lists based on complexity level
        if complexity == 0:
            char_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        elif complexity == 1:
            char_list = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        elif complexity == 2:
            char_list = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [str(i) for i in range(10)]
        elif complexity == 3:
            char_list = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [str(i) for i in range(10)]

        # generate password
        password = ''.join(random.choices(char_list, k=length))
        
        return password
    
    def generate_token(self, payload: Dict[str, Any]) -> str:
        """Generates a JWT token with the given payload."""
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token.decode('utf-8')

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decodes a JWT token and returns the payload."""
        payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        return payload