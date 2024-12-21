class Query:

    @staticmethod
    def create_chat():
        return """
        CREATE (c:Chat{id: $id, user_id: $user_id theme: $theme, system_instruction: $system_instruction, temperature: $temperature, max_output_tokens: $max_output_tokens, create_date: $create_date})
        """

    @staticmethod
    def create_user():
        return """
        CREATE (c:User{id: $id, user_class: $user_class, tg_id: $tg_id, username: $username, create_data: $create_date})
        """

    @staticmethod
    def create_relation(node1: str, node2: str, relation: str):
        return f"""
        MATCH ({node1}-[:{relation}]->({node2}))
        """

    @staticmethod
    def create_and_relate_user_to_chat():
        return """
        CREATE (c:Chat{id: $id, user_id: $user_id, class_chat: $class_chat, theme: $theme, system_instruction: $system_instruction, temperature: $temperature, max_output_tokens: $max_output_tokens, create_date: $create_date})
        CREATE (u:User {id: $user_id, user_class: $user_class, tg_id: $tg_id, username: $username, create_data: $create_date})
        MERGE (u)-[:OWNER]->(c)
        """


    @staticmethod
    def create_request():
        return """
        CREATE (r:Request {id: $id, user_id: $user_id, chat_id: $chat_id, model: $model, prompt: $prompt, file_url: $file_url, token_len: $token_len, token_cost: $token_cost, create_date: $create_date})
        WITH r
        MATCH (c:Chat {id: $chat_id})
        MERGE (c)-[:POST]->(r)
        """
