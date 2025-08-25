import re
import json
import demjson3


class Validator:

    @classmethod
    def extract_json_from_ai_response(cls, ans):
            print("generated answer-----------------", ans)
            cleaned_text = re.sub(r"```json\s*([\s\S]*?)```", r"\1", ans, flags=re.MULTILINE)

            # If the above doesn't catch, also try removing any backticks wrapping whole string
            cleaned_text = cleaned_text.strip('` \n\r\t')

            # Fix misplaced quotes like: "sentence", more text
            # cleaned_text = re.sub(r'\"([^\"]+)\"\,', lambda m: '"' + m.group(1).replace('"', '\\"') + '",', cleaned_text)

            # cleaned_text = cleaned_text.replace('undefined', 'null')
            # cleaned_text = re.sub(r"\)\s*{", "{", cleaned_text)
            # cleaned_text = re.sub(r",\s*([}\]])", r"\1", cleaned_text)  # trailing commas

            # Add missing commas between } {
            # cleaned_text = re.sub(r'}\s*{', '}, {', cleaned_text)
            # # Remove trailing commas before ]
            # cleaned_text = re.sub(r',\s*]', ']', cleaned_text)
            # # Remove trailing commas before }
            # cleaned_text = re.sub(r',\s*}', '}', cleaned_text)

            # cleaned_text = re.sub(r'"\s*([a-zA-Z0-9_]+)"\s*:', r'", "\1":', cleaned_text)  # Add missing comma before new key
            print("cl3aned text-----------", cleaned_text)
            # print("cleaned_text", cleaned_text)
            # # Try full JSON decode first
            # try:
            #     print("inside first try")
            #     return json.loads(cleaned_text)
            # except json.JSONDecodeError:
            #     pass


            # # Now parse cleaned JSON string
            # try:
            #     data = demjson3.decode(cleaned_text)
            #     return data
            # except Exception as e:
            #     print(f"Error parsing JSON: {e}")
            #     return None


            # Fallback to demjson3 for more lenient parsing
            try:
                # import json

                # def escape_json_string_values(data):
                #     if isinstance(data, dict):
                #         return {k: escape_json_string_values(v) for k, v in data.items()}
                #     elif isinstance(data, list):
                #         return [escape_json_string_values(i) for i in data]
                #     elif isinstance(data, str):
                #         return data.replace('\n', '\\n')
                #     else:
                #         return data

                # # Assuming `json_data` is the object you're sending
                # escaped_data = escape_json_string_values(cleaned_text)
                # escaped_json = json.dumps(escaped_data)
                # print("escaped one json", escaped_json)
                # return escaped_json
                print("in seocnd try demjson")
                parsed = demjson3.decode(cleaned_text)
                if isinstance(parsed, list):
                    return parsed
                else:
                    return parsed
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return None


            # Last resort — extract objects individually if even demjson3 fails
            # chunks = re.findall(r'{[^{}]*"question_number"[^{}]*}', cleaned_text, re.DOTALL)
            # valid = []
            # errors = []
            # print(chunks)
            # for chunk in chunks:
            #     print("in chunk", chunk)
            #     try:
            #         obj = demjson3.decode(chunk)
            #         valid.append(obj)
            #     except Exception as e:
            #         errors.append({'chunk': chunk, 'error': str(e)})
            #         print("in last exception------", errors)
            # return valid