user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 4
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "anyOf": [
                {"pattern": ".*[0-9].*"},
                {"pattern": ".*[!@#$%^&*()_\\-+=~`\\[\\]{}|\\\\:;\"'<>,.?/].*"}
            ]
        },
        "email": {
            "title": "Email address",
            "type": "string",
            "pattern": "^\\S+@\\S+\\.\\S+$",
            "format": "email",
            "minLength": 6,
            "maxLength": 127
        }
    },
    "required": ["name", "email", "password"],
}
